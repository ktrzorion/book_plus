from flask import Flask, Blueprint, send_file, abort
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.orm import aliased
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from sqlalchemy import or_, distinct
from flask_jwt_extended import decode_token
import numpy as np
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    get_jwt_identity,
    create_access_token,
    get_jwt,
    set_access_cookies,
    unset_jwt_cookies
)
from datetime import datetime
from sqlalchemy.sql import func
from functools import wraps
import base64
from datetime import datetime, timedelta
import imghdr
from config import Config
from PIL import Image
from io import BytesIO
from flask import jsonify, request
from flask_mail import Mail
from celery_conf import celery_init_app
from html import escape
from PyPDF2 import PdfReader
from datetime import timedelta, timezone
from flask_caching import Cache
import matplotlib.pyplot as plt
import logging
# from tabulate import tabulate

app = Flask(__name__)
app.config.from_object(Config)

# import pdb
# pdb.set_trace()
# LOGGING SETUP
logging.basicConfig(level=logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logging.getLogger().addHandler(stream_handler)

app.config.from_object(Config)

cache = Cache(app)

app.config.from_mapping(
    CELERY=dict(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        task_ignore_result=True,
    ),
)

CORS(app)

from models import (
    db,
    User,
    Section,
    Content,
    Borrowing,
    TransactionLog,
    ContentReview,
    Wishlist,
    LoginData,
    PurchaseData,
    IssueRequest
)
# Initialize Flask extensions
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
cache = Cache(app)

celery_app = celery_init_app(app)

# Create Flask-Mail instance
mail = Mail(app)


migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

blacklisted_tokens = set()

def get_current_user():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    return current_user

# ROUTE - REGISTER
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        hashed_password = bcrypt.generate_password_hash(data["password"]).decode(
            "utf-8"
        )

        new_user = User(
            firstname=data["firstname"],
            lastname=data["lastname"],
            username=data["username"],
            phoneNumber=data["phoneNumber"],
            email=data["email"],
            password=hashed_password,
            gender=data["gender"],
            address=data["address"],
            city=data["city"],
            state=data["state"],
            zip=data["zip"],
            role=data["role"],
        )

        db.session.add(new_user)
        db.session.commit()

        app.logger.info('User Registered Successfully')
        return jsonify({"message": "Registration successful"}), 201
    except Exception as e:
        app.logger.error('User Registered Failed')
        return jsonify({"error": "Registration failed", "details": str(e)}), 500


# ROUTE - LOGIN
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        user = User.query.filter(
            or_(User.email == data["input"], User.username == data["input"])
        ).first()

        if user and bcrypt.check_password_hash(user.password, data["password"]):

            login_data = LoginData.query.filter_by(user_id=user.id).first()

            if login_data:
                login_data.last_login_time = datetime.now()
            else:
                login_data = LoginData(
                    user_id=user.id, last_login_time=datetime.now()
                )
                db.session.add(login_data)

            db.session.commit()

            additional_claims = {
                "id": user.id,
                "role": user.role,
                "username": user.username,
                "email": user.email,
            }
            access_token = create_access_token(
                identity=user.id, additional_claims=additional_claims
            )

            app.logger.info("Login Successful")
            return jsonify({"message": "Login successful", "token": access_token}), 200
        else:
            app.logger.warning("Incorrect Login Details")
            return jsonify({"error": "Invalid email/username or password"}), 401
    except Exception as e:
        app.logger.error("Error Logging In")
        return jsonify({"error": "Login failed", "details": str(e)}), 500


# Custom decorator to check if a token is in the blacklist
def token_not_in_blacklist(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        jti = get_jwt()["jti"]
        if jti in blacklisted_tokens:
            return jsonify({"error": "Token has been revoked"}), 401
        return fn(*args, **kwargs)

    return wrapper

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    jti = jwt_data['jti']
    return jti in blacklisted_tokens

# ROUTE - LOGOUT
@app.route("/logout", methods=["POST"])
@jwt_required()
@token_not_in_blacklist
def logout():
    try:
        jti = get_jwt()["jti"]

        blacklisted_tokens.add(jti)
        unset_jwt_cookies()

        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        return jsonify({"error": "Logout failed", "details": str(e)}), 500


@app.route("/verify", methods=["OPTIONS"])
def handle_options():
    response = jsonify({"message": "CORS preflight request successful"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    return response


# ROUTE - VERIFY TOKEN AND GET USER INFO
@app.route("/verify", methods=["GET"])
def verify_token():
    try:
        token = request.headers.get("Authorization")
        user = validate_token_and_get_user(token)

        if user:
            app.logger.info("User Present")
            return (
                jsonify(
                    {
                        "authenticated": True,
                        "user": {"id": user.id, "username": user.username, "role": user.role},
                    }
                ),
                200,
            )
        else:
            app.logger.warning("No User Found")
            return jsonify({"authenticated": False}), 401

    except Exception as e:
        app.logger.info("Error Verifying Token")
        return jsonify({"error": "Error verifying token", "details": str(e)}), 500


def validate_token_and_get_user(token):
    try:
        if token:

            @jwt_required()
            def get_user_from_token():
                user_id = get_jwt_identity()
                user = User.query.filter_by(id=user_id).first()
                return user

            return get_user_from_token()
        else:
            return None
    except Exception as e:
        print("Exception during token validation:", str(e))
        return None


# ROUTE - CREATE NEW Section
@app.route("/section", methods=["POST"])
@jwt_required()
def create_section():
    try:
        data = request.get_json()

        existing_Section = Section.query.filter_by(name=data["name"]).first()
        if existing_Section:
            return jsonify({"error": "Section already exists"}), 400

        new_section = Section(name=data["name"])
        db.session.add(new_section)
        db.session.commit()

        return jsonify({"message": "Section created successfully"}), 201
    except Exception as e:
        return jsonify({"error": "Section creation failed", "details": str(e)}), 500


# Fetch Sections
@app.route("/fetch-sections", methods=["GET"])
def get_all_sections():
    try:
        sections = Section.query.all()

        # Convert the sections to a list of dictionaries
        sections_list = [
            {"id": section.id, "name": section.name} for section in sections
        ]

        app.logger.info("Fetched Sections")
        return jsonify({"sections": sections_list})
    except Exception as e:
        app.logger.error("Fetching Sections Failed")
        return jsonify({"error": "Failed to fetch sections", "details": str(e)}), 500


# ROUTE - DELETE Section
@app.route("/remove-section/<int:section_id>", methods=["DELETE"])
@jwt_required()
def delete_section(section_id):
    try:
        section = Section.query.get(section_id)

        if section:
            # Delete all content associated with the section
            Content.query.filter_by(section=section_id).delete()

            # Now delete the section itself
            db.session.delete(section)
            db.session.commit()
            app.logger.info("Section Deletion Success")
            return jsonify({"message": "Section and associated content deleted successfully"}), 200
        else:
            app.logger.warning("Failed Deleting Section")
            return jsonify({"error": "Section not found"}), 404
    except IntegrityError:
        db.session.rollback()
        app.logger.error("Error Deleting Section: IntegrityError")
        return jsonify({"error": "Section deletion failed due to integrity error"}), 500
    except Exception as e:
        app.logger.error("Error Deleting Section", str(e))
        return jsonify({"error": "Section deletion failed", "details": str(e)}), 500

# ROUTE - FETCH Section Data For Update
@app.route("/get-section/<int:section_id>", methods=["GET"])
@jwt_required()
def get_section(section_id):
    try:
        section = Section.query.get(section_id)

        if section:
            return jsonify({"name": section.name}), 200
        else:
            return jsonify({"error": "Section not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to fetch section", "details": str(e)}), 500

# ROUTE - UPDATE SECTION
@app.route("/update-section/<int:section_id>", methods=["PUT"])
@jwt_required()
def update_section(section_id):
    section = Section.query.get(section_id)

    data = request.get_json()
    existing_Section = Section.query.filter_by(name=data["name"]).first()
    if existing_Section:
        app.logger.warning("Section Already Exist")
        return jsonify({"error": "Section already exists"}), 400

    new_name = data.get("name")

    if not new_name:
        app.logger.error("Enter Section Name")
        return jsonify({"error": "Name is required"}), 400

    section.name = new_name
    db.session.commit()

    app.logger.info("Section Updated to: ", new_name)
    return jsonify({"message": "Section updated successfully"})


# Function to get the image type based on magic number
def get_image_type(image_data):
    try:
        image_pil = Image.open(BytesIO(image_data))
        return image_pil.format.lower()
    except Exception as e:
        print(e)
        return None


# ROUTE - ADD CONTENT
@app.route("/add-content/<int:section_id>/<int:user_id>", methods=["POST"])
@jwt_required()
def add_content(section_id, user_id):

    current_user_id = get_jwt_identity()

    if current_user_id != user_id:
        app.logger.error("User is unauthorized")
        return jsonify({"message": "Unauthorized"}), 401

    section = Section.query.get(section_id)
    if not section:
        app.logger.error("Section Not Found")
        return jsonify({"message": "Invalid section_id"}), 400
    
    # Check if image and pdf files are present in the request
    if 'image' not in request.files:
        app.logger.error("Image file is missing")
        return jsonify({"message": "Image file is required"}), 400

    if 'pdf' not in request.files:
        app.logger.error("PDF file is missing")
        return jsonify({"message": "PDF file is required"}), 400

    try:
        title = escape(request.form.get("title"))
        author = escape(request.form.get("author"))
        number_of_pages = escape(request.form.get("number_of_pages"))
        price = escape(request.form.get("price"))
        publish_year = escape(request.form.get("publish_year"))

        if not all([title, author, number_of_pages, publish_year, price, ]):
            app.logger.warn("Data Is Incomplete")
            return jsonify({"message": "Incomplete form data"}), 400

        content = Content(
            title=title,
            author=author,
            number_of_pages=number_of_pages,
            publish_year=publish_year,
            price=price,
            section=section_id,
            uploaded_by_id=user_id,
        )

        if "image" in request.files:
            image = request.files["image"]
            if image:
                filename = secure_filename(image.filename)
                image_data = image.read()
                image_type = imghdr.what(None, h=image_data)
                content.image = image_data
                content.imageType = image_type

        if "pdf" in request.files:
            pdf = request.files["pdf"]
            if pdf:
                filename = secure_filename(pdf.filename)
                pdf_data = pdf.read()

                # Validate the PDF file using PyPDF2
                try:
                    pdf_reader = PdfReader(pdf)
                    if len(pdf_reader.pages) == 0:
                        app.logger.warning("No Pages Available In PDF")
                        return (
                            jsonify({"message": "Invalid PDF file: No pages found"}),
                            400,
                        )
                    else:
                        content.number_of_pages = len(pdf_reader.pages)
                except Exception as e:
                    app.logger.error("Invalid PDF File")
                    return jsonify({"message": f"Invalid PDF file: {str(e)}"}), 400

                content.pdf_file_name = filename
                content.file = pdf_data
        else:
            content.file = None

        db.session.add(content)
        db.session.commit()

        app.logger.info("Content Added Successfully")
        return jsonify({"message": "Content added successfully"}), 201

    except Exception as e:
        app.logger.error("Error Adding Content", str(e))
        return jsonify({"message": f"Error adding content: {str(e)}"}), 500


# ROUTE - DELETE Content
@app.route("/delete-content/<int:content_id>", methods=["DELETE"])
@jwt_required()
def delete_content(content_id):
    try:
        content = Content.query.get(content_id)

        if content:
            related_wishlist_items = Wishlist.query.filter_by(content_id=content_id).all()

            # Delete wishlist items related to the content
            for wishlist_item in related_wishlist_items:
                db.session.delete(wishlist_item)

            # Delete the content
            db.session.delete(content)
            db.session.commit()

            app.logger.info("Content and related wishlist items deleted successfully")
            return jsonify({"message": "Content and related wishlist items deleted successfully"}), 200
        else:
            app.logger.warn("Content Not Found")
            return jsonify({"error": "Content not found"}), 404
    except Exception as e:
        app.logger.error("Error Deleting Content", str(e))
        return jsonify({"error": "Content deletion failed", "details": str(e)}), 500


# ROUTE - UPDATE CONTENT
@app.route("/update-content/<int:content_id>/<int:user_id>", methods=["POST"])
@jwt_required()
def update_content(content_id, user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        app.logger.warn("User Is Unauthorized")
        return jsonify({"message": "Unauthorized"}), 401

    try:
        content = Content.query.get(content_id)

        title = request.form.get("title")
        author = request.form.get("author")
        number_of_pages = request.form.get("number_of_pages")
        publish_year = request.form.get("publish_year")
        price = request.form.get("price")

        if not all([title, author, number_of_pages, publish_year]):
            app.logger.warn("Incomplete Data")
            return jsonify({"message": "Incomplete form data"}), 400

        content.title = title
        content.author = author
        content.number_of_pages = number_of_pages
        content.publish_year = publish_year
        content.price = price

        if "image" in request.files:
            image = request.files["image"]
            if image:
                filename = secure_filename(image.filename)

                image_data = image.read()

                image_type = imghdr.what(None, h=image_data)

                content.image = image_data
                content.imageType = image_type
        
        if "pdf" in request.files:
            pdf = request.files["pdf"]
            if pdf:
                filename = secure_filename(pdf.filename)
                pdf_data = pdf.read()

                # Validate the PDF file using PyPDF2
                try:
                    pdf_reader = PdfReader(pdf)
                    if len(pdf_reader.pages) == 0:
                        return (
                            jsonify({"message": "Invalid PDF file: No pages found"}),
                            400,
                        )
                    else:
                        content.number_of_pages = len(pdf_reader.pages)
                except Exception as e:
                    app.logger.error("Invalid PDF File")
                    return jsonify({"message": f"Invalid PDF file: {str(e)}"}), 400

                content.pdf_file_name = filename
                
                # Only update the file if a new PDF file is provided
                content.file = pdf_data

        db.session.commit()

        app.logger.info("Content Updated Successfully")
        return jsonify({"message": "Content updated successfully"}), 201

    except Exception as e:
        app.logger.error("Error Updating Content")
        return jsonify({"message": "Error updating content"}), 500

# ROUTE - FETCH CONTENT
@app.route("/fetch-content", methods=["GET"])
def fetch_content():
    try:
        contents = Content.query.all()

        formatted_contents = []
        for content in contents:
            ratings = ContentReview.query.filter_by(content_id=content.id).all()
            average_rating = round(sum(rating.rating for rating in ratings) / len(ratings), 2) if ratings else 0

            formatted_content = {
                "id": content.id,
                "title": content.title,
                "author": content.author,
                "rating": average_rating,
                "section": content.section,
                "imageType": content.imageType,
                "image": base64.b64encode(content.image).decode("utf-8"),
                "ratings": [
                    {
                        "id": rating.id,
                        "rating": rating.rating,
                        "comment": rating.comment,
                        "user_id": rating.user_id
                    }
                    for rating in ratings
                ]
            }
            formatted_contents.append(formatted_content)

        app.logger.info("Content Fetched Successfully")
        return jsonify({"contents": formatted_contents})

    except Exception as e:
        app.logger.error("Error Fetching Content", str(e))
        return jsonify({"error": "Failed to fetch content", "details": str(e)}), 500
    
# ROUTE - TOP 15 CONTENT
@app.route('/fetch-top15', methods=['GET'])
def fetch_top15_contents():
    try:
        # Query the top 15 contents sorted by average rating
        top15_contents = db.session.query(Content, func.avg(ContentReview.rating).label('avg_rating')) \
            .join(ContentReview) \
            .group_by(Content.id) \
            .order_by(func.avg(ContentReview.rating).desc()) \
            .limit(15) \
            .all()

        # Serialize the contents
        serialized_contents = []
        for content, avg_rating in top15_contents:
            serialized_content = {
                'id': content.id,
                'title': content.title,
                'author': content.author,
                'rating': round(avg_rating or 0, 2),
                'image': content.image,
                'imageType': content.imageType,
                "image": base64.b64encode(content.image).decode("utf-8"),
                'average_rating': avg_rating
            }
            serialized_contents.append(serialized_content)
        
        app.logger.info("Fetched Top15 Content Successfully")
        return jsonify({'contents': serialized_contents}), 200
    except Exception as e:
        app.logger.error("Error Fetching Top15 Content", str(e))
        return jsonify({'error': str(e)}), 500

# ROUTE - FETCH CONTENT ON USER ID
@app.route("/user/fetch-content/<int:user_id>", methods=["GET"])
def fetch_user_content(user_id):
    try:
        contents = (
            Content.query.outerjoin(
                Borrowing,
                (Borrowing.content_id == Content.id) & (Borrowing.member_id == user_id),
            )
            .outerjoin(
                Wishlist,
                (Wishlist.content_id == Content.id) & (Wishlist.user_id == user_id),
            )
            .outerjoin(ContentReview, ContentReview.content_id == Content.id)
            .outerjoin(
                IssueRequest,
                (IssueRequest.contentId == Content.id) & (IssueRequest.userId == user_id),
            )
            .add_columns(
                Content.id,
                Content.title,
                Content.author,
                Content.section,
                func.avg(ContentReview.rating).label("rating"),
                Content.imageType,
                Content.image,
                Borrowing.returned.label("returned"),
                Borrowing.id.label("borrowing_id"),
                Wishlist.id.label("wishlist_id"),
                IssueRequest.response.label("isRequested"),
            )
            .group_by(Content.id)
            .all()
        )

        formatted_contents = [
            {
                "id": content.id,
                "title": content.title,
                "author": content.author,
                "section": content.section,
                "rating": round(content.rating or 0, 2),
                "imageType": content.imageType,
                "image": base64.b64encode(content.image).decode("utf-8"),
                "isIssued": content.borrowing_id is not None and not content.returned,
                "isWishlisted": content.wishlist_id is not None,
                "isRead": content.borrowing_id is not None,
                "isRequested": content.isRequested == 'Pending' if content.isRequested else False
            }
            for content in contents
        ]
        app.logger.info("Content Fetched On User-ID Successful")

        return jsonify({"contents": formatted_contents})

    except Exception as e:
        app.logger.error("Content Fetched On User-ID Failed: %s", str(e))
        return ( 
            jsonify({"error": "Failed to fetch user content", "details": str(e)}),
            500,
        )

# # ROUTE - FETCH CONTENT ON USER ID AND CONTENT ID
# @app.route("/user/fetch-content/<int:user_id>/<int:content_id>", methods=["GET"])
# def fetch_userid_content_id_content(user_id, content_id):
#     try:
#         content = (
#             Content.query.filter_by(id=content_id)
#             .outerjoin(
#                 Borrowing,
#                 (Borrowing.content_id == Content.id) & (Borrowing.member_id == user_id),
#             )
#             .outerjoin(
#                 Wishlist,
#                 (Wishlist.content_id == Content.id) & (Wishlist.user_id == user_id),
#             )
#             .outerjoin(ContentReview, ContentReview.content_id == Content.id)
#             .outerjoin(
#                 IssueRequest,
#                 (IssueRequest.contentId == Content.id) & (IssueRequest.userId == user_id),
#             )
#             .add_columns(
#                 Content.id,
#                 Content.title,
#                 Content.author,
#                 Content.section,
#                 func.avg(ContentReview.rating).label("rating"),
#                 Content.imageType,
#                 Content.image,
#                 Borrowing.returned.label("returned"),
#                 Borrowing.id.label("borrowing_id"),
#                 Wishlist.id.label("wishlist_id"),
#                 case((IssueRequest.response.is_(None), True), else_=False).label("isRequested"),
#             )
#             .group_by(Content.id)
#             .first()
#         )

#         if content:
#             formatted_content = {
#                 "id": content.id,
#                 "title": content.title,
#                 "author": content.author,
#                 "section": content.section,
#                 "rating": round(content.rating or 0, 2),
#                 "imageType": content.imageType,
#                 "image": base64.b64encode(content.image).decode("utf-8"),
#                 "isIssued": content.borrowing_id is not None and not content.returned,
#                 "isWishlisted": content.wishlist_id is not None,
#                 "isRead": content.borrowing_id is not None,
#                 "isRequested": content.isRequested or False,
#             }
#             app.logger.info("Content Fetched On User-ID & Content-ID Successful")
#             return jsonify({"content": formatted_content})
#         else:
#             app.logger.warning("Content Fetched On User-ID & Content-ID -->> Content Not Found")
#             return jsonify({"error": "Content not found"}), 404

#     except Exception as e:
#         app.logger.error("Content Fetched On User-ID & Content-ID Failed: %s", str(e))
#         return (
#             jsonify({"error": "Failed to fetch user content", "details": str(e)}),
#             500,
#         )

# ROUTE - FETCH CONTENT DETAILS FOR - UPDATE
@app.route("/fetch-content-details/<int:content_id>", methods=["GET"])
@jwt_required()
def fetch_content_details(content_id):
    content = Content.query.get(content_id)

    if content:
        content_details = {
            "image": base64.b64encode(content.image).decode("utf-8"),
            "title": content.title,
            "author": content.author,
            "price": content.price,
            "publish_year": content.publish_year,
        }

        app.logger.info("Content Fetched On Content-ID Successfully")
        return jsonify(content_details)
    else:
        app.logger.error("Content Fetched On Content-ID Failed")
        return jsonify({"message": "Content not found"}), 404


# ROUTE - ACTIVITY
@app.route("/activity-data/<int:content_id>", methods=["GET"])
@jwt_required()
def get_activity_data(content_id):
    try:
        query_result = (
            db.session.query(
                Borrowing.content_id,
                Content.title,
                User.username,
                Section.name.label("section_name"),
                Borrowing.borrow_date,
                Borrowing.returned,
                Borrowing.last_return_date,
                Borrowing.reissue_count,
                User.id.label("user_id"),
            )
            .join(User, User.id == Borrowing.member_id)
            .join(Content, Content.id == Borrowing.content_id)
            .join(Section, Section.id == Content.section)
            .filter(Borrowing.content_id == content_id, Borrowing.returned == False)
            .all()
        )

        result_data = [
            {
                "user_id": row.user_id,
                "content_id": row.content_id,
                "title": row.title,
                "username": row.username,
                "section_name": row.section_name,
                "borrow_date": row.borrow_date.strftime("%Y-%m-%d %H:%M:%S"),
                "returned": row.returned,
                "last_return_date": (
                    row.last_return_date.strftime("%Y-%m-%d %H:%M:%S")
                    if row.last_return_date
                    else None
                ),
                "reissue_count": row.reissue_count,
                "user_id": row.user_id,
            }
            for row in query_result
        ]

        app.logger.info("Activity Data Fetched Successfully")
        return jsonify(result_data)

    except Exception as e:
        app.logger.error("Error Fetching Activity Data")
        return jsonify({"error": str(e)}), 500
    
# ROUTE - FETCH ACTIVITY COUNT DATA
@app.route('/current-reader-count/<int:content_id>', methods=['GET'])
@jwt_required()
def current_reader_count(content_id):
    try:
        current_count = Borrowing.query.filter_by(content_id=content_id, returned=False).distinct(Borrowing.member_id).count()
        app.logger.info("Current Reader Count Fetched")
        return jsonify({'currentReaderCount': current_count}), 200
    except Exception as e:
        app.logger.error("Error Fetching CRC", str(e))
        return jsonify({'error': str(e)}), 500

# ROUTE - Fetch Reader Count
@app.route('/total-reader-count/<int:content_id>', methods=['GET'])
@jwt_required()
def total_reader_count(content_id):
    try:
        total_count = Borrowing.query.filter_by(content_id=content_id).distinct(Borrowing.member_id).count()
        app.logger.info("Total Reader Count Fetched")
        return jsonify({'totalReaderCount': total_count}), 200
    except Exception as e:
        app.logger.error("Error Fetching TRC", str(e))
        return jsonify({'error': str(e)}), 500

# ROUTE - Fetch Wishlist Count
@app.route('/wishlist-count/<int:content_id>', methods=['GET'])
@jwt_required()
def wishlist_count(content_id):
    try:
        count = Wishlist.query.filter_by(content_id=content_id).count()
        app.logger.info("Wishlist Count Fetched")
        return jsonify({'wishlistCount': count}), 200
    except Exception as e:
        app.logger.error("Error Fetching WC", str(e))
        return jsonify({'error': str(e)}), 500

# ROUTE - ACCEPT ISSUE REQUEST
@app.route("/accept_request/<int:content_id>/<int:user_id>", methods=["POST"])
@jwt_required()
def accept_request(content_id, user_id):
    try:
        current_user_id = user_id

        content = Content.query.get(content_id)

        if not content:
            app.logger.warn("No Such Content Found To Borrow")
            return jsonify({"error": "Content not found"}), 404

        total_borrowing = Borrowing.query.filter_by(
            member_id=current_user_id, returned=False
        ).count()

        if total_borrowing == 5:
            app.logger.warn("Borrowing Limit Reached")
            return jsonify({"error": "User has reached borrowing limit of 5."}), 400

        existing_borrowing = Borrowing.query.filter_by(
            content_id=content_id, member_id=current_user_id, return_date=None
        ).first()

        if existing_borrowing:
            app.logger.warn("Content Already Borrowed")
            return jsonify({"error": "User has already borrowed this Content"}), 400

        new_borrowing = Borrowing(
            content_id=content_id, member_id=current_user_id, borrow_date=datetime.now()
        )
        
        db.session.add(new_borrowing)

        new_borrowing.last_return_date = new_borrowing.borrow_date + timedelta(days=7)

        issue_request = IssueRequest.query.filter_by(contentId=content_id, userId=user_id).first()
        if issue_request:
            issue_request.response = "Accepted"
            db.session.commit()
        else:
            app.logger.warn("Issue Request not found for the specified content and user")

        new_transaction_log = TransactionLog(
            user_id=current_user_id,
            action="Issue",
            content_id=content_id,
            timestamp=datetime.now(),
        )

        db.session.add(new_transaction_log)

        # Update the IssueRequest response to "Accepted"

        db.session.commit()

        app.logger.info("Content Borrowed Sucessfully")
        return jsonify({"message": "Content issued successfully"}), 200
    except Exception as e:
        app.logger.error("Error Borrowing Content", str(e))
        return jsonify({"error": "Issuing content failed", "details": str(e)}), 500

# ROUTE - RETURN CONTENT
@app.route("/return_content/<int:content_id>", methods=["POST"])
@jwt_required()
def return_content(content_id):
    try:
        current_user_id = get_jwt_identity()

        borrowing = Borrowing.query.filter_by(
            content_id=content_id, member_id=current_user_id, returned=False
        ).first()

        print(content_id, current_user_id, borrowing)

        if not borrowing:
            app.logger.warn("Borrowing Record Not Found / Already Returned")
            return (
                jsonify({"error": "Borrowing record not found or already returned"}),
                404,
            )

        borrowing.returned = True
        borrowing.return_date = datetime.now()
        borrowing.late = (
            borrowing.last_return_date
            and datetime.now() > borrowing.last_return_date
        )

        # Delete IssueRequest
        issue_request = IssueRequest.query.filter_by(contentId=content_id, userId=current_user_id).first()
        if issue_request:
            db.session.delete(issue_request)

        new_transaction_log = TransactionLog(
            user_id=current_user_id,
            action="Return",
            content_id=borrowing.content_id,
            timestamp=datetime.now(),
        )
        db.session.add(new_transaction_log)

        db.session.commit()

        app.logger.info("Content Returned Successfully")
        return jsonify({"message": "Content returned successfully"}), 200
    except Exception as e:
        app.logger.error("Error Returning Content", str(e))
        return jsonify({"error": "Returning content failed", "details": str(e)}), 500

# ROUTE - REISSUE CONTENT - UNDER MAINTAINANCE
@app.route("/reissue_content/<int:borrowing_id>", methods=["POST"])
@jwt_required()
def reissue_content(borrowing_id):
    try:
        current_user_id = get_jwt_identity()

        borrowing = Borrowing.query.filter_by(
            id=borrowing_id, member_id=current_user_id, return_date=None
        ).first()

        if not borrowing:
            app.logger.warn("Borrowing Record Not Found / Already Returned")
            return (
                jsonify({"error": "Borrowing record not found or already returned"}),
                404,
            )

        if borrowing.reissue_count >= 3:
            app.logger.warning("Re-Issue Limit Reached")
            return jsonify({"error": "Maximum reissue limit reached"}), 400

        borrowing.reissue_count += 1
        borrowing.estimated_return_date = borrowing.last_return_date + timedelta(days=7)
        borrowing.last_return_date = datetime.now()

        new_transaction_log = TransactionLog(
            user_id=current_user_id,
            action="Re-Issue",
            content_id=borrowing_id,
            timestamp=datetime.now(),
        )
        db.session.add(new_transaction_log)

        db.session.commit()

        app.logger.info("Content Reissue Successful")
        return jsonify({"message": "Content reissued successfully"}), 200
    except Exception as e:
        app.logger.warn("Content Reissue Failed", str(e))
        return jsonify({"error": "Reissuing content failed", "details": str(e)}), 500

# ROUTE - ADD TO WISHLIST
@app.route("/wishlist/add/<int:content_id>", methods=["POST"])
@jwt_required()
def add_to_wishlist(content_id):
    try:
        current_user_id = get_jwt_identity()

        existing_wishlist_item = Wishlist.query.filter_by(
            content_id=content_id, user_id=current_user_id
        ).first()

        if existing_wishlist_item:
            app.logger.warn("Content Already In Wishlist")
            return jsonify({"error": "Content is already in the wishlist"}), 400

        new_wishlist_item = Wishlist(content_id=content_id, user_id=current_user_id)
        db.session.add(new_wishlist_item)

        new_transaction_log = TransactionLog(
            user_id=current_user_id,
            action="+ Wishlist",
            content_id=content_id,
            timestamp=datetime.now(),
        )
        db.session.add(new_transaction_log)

        db.session.commit()

        app.logger.info("Content Wishlisted Successfully")
        return jsonify({"message": "Content added to wishlist successfully"}), 200
    except Exception as e:
        app.logger.error("Content Wishlisting Failed", str(e))
        return (
            jsonify({"error": "Failed to add content to wishlist", "details": str(e)}),
            500,
        )

# ROUTE - REMOVE FROM WISHLIST
@app.route("/wishlist/remove/<int:content_id>", methods=["POST"])
@jwt_required()
def remove_from_wishlist(content_id):
    try:
        current_user_id = get_jwt_identity()

        wishlist_item = Wishlist.query.filter_by(
            content_id=content_id, user_id=current_user_id
        ).first()

        if not wishlist_item:
            app.logger.warn("Content Not Found In Wishlisted")
            return jsonify({"error": "Content not found in the wishlist"}), 404

        db.session.delete(wishlist_item)

        new_transaction_log = TransactionLog(
            user_id=current_user_id,
            action="- Wishlist",
            content_id=content_id,
            timestamp=datetime.now(),
        )
        db.session.add(new_transaction_log)

        db.session.commit()

        app.logger.info("Content Removed From Wishlist Successfully")
        return jsonify({"message": "Content removed from wishlist successfully"}), 200
    except Exception as e:
        app.logger.error("Error Removing Content From Wishlist", str(e))
        return (
            jsonify(
                {"error": "Failed to remove content from wishlist", "details": str(e)}
            ),
            500,
        )

# ROUTE - VIEW TRANSACTION LOGS
@app.route("/transaction_logs", methods=["GET"])
@jwt_required()
def get_transaction_logs():
    try:
        logs = TransactionLog.query.all()

        serialized_logs = []
        for log in logs:
            serialized_log = {
                "id": log.id,
                "user_id": log.user_id,
                "action": log.action,
                "content_id": log.content_id,
                "timestamp": log.timestamp.isoformat(),
            }
            serialized_logs.append(serialized_log)

        app.logger.info("Transaction Logs Fetched")
        return jsonify({"transaction_logs": serialized_logs})

    except Exception as e:
        app.logger.info("Error Fetching Transaction Logs", str(e))
        return jsonify({"error": str(e)}), 500

# FETCH - PDF FILE
@app.route('/get_pdf/<int:content_id>')
@cache.cached(timeout=60)
@jwt_required()
def get_pdf(content_id):
    try:
        content = Content.query.get_or_404(content_id)

        pdf_blob = content.file

        pdf_bytes = BytesIO(pdf_blob)

        app.logger.info("PDF File Fetched")

        return send_file(pdf_bytes, mimetype='application/pdf', as_attachment=False)
    
    except Exception as e:
        app.logger.error("Error Fetching PDF File", str(e))
        return jsonify({"error": str(e)}), 500

# ROUTE - REVOKE ACCESS
@app.route("/revoke-access", methods=["POST"])
@jwt_required()
def revoke_access():
    data = request.get_json()

    content_id = data.get("contentId")
    user_id = data.get("userId")

    borrowing_record = Borrowing.query.filter_by(
        content_id=content_id, member_id=user_id
    ).first()

    if borrowing_record:
        borrowing_record.returned = True
        borrowing_record.return_date = datetime.now()

        # Delete IssueRequest
        issue_request = IssueRequest.query.filter_by(contentId=content_id, userId=user_id).first()
        if issue_request:
            db.session.delete(issue_request)

        new_transaction_log = TransactionLog(
            user_id=user_id,
            action="Revoke",
            content_id=content_id,
            timestamp=datetime.now(),
        )

        db.session.add(new_transaction_log)
        db.session.commit()

        app.logger.info("Access Revoked Successfully For User: %s & Content: %s", user_id, content_id)
        return jsonify({"message": "Access revoked successfully"})
    else:
        app.logger.error("Error Revoking Access")
        return jsonify({"error": "Borrowing record not found"}), 404
    
# ROUTE - RATING
@app.route('/rate_content/<int:content_id>', methods=['POST'])
@jwt_required()
def rate_content(content_id):
    try:
        data = request.json
        rating_value = data.get('rating')
        comment = data.get('comment')

        user_id = get_jwt_identity()

        rating = ContentReview.query.filter_by(content_id=content_id, user_id=user_id).first()
        new_transaction_log = TransactionLog(
                user_id=user_id,
                action="New Content Review",
                content_id=content_id,
                timestamp=datetime.now(),
            )

        db.session.add(new_transaction_log)
        db.session.commit()
        
        if rating:
            rating.rating = rating_value
            rating.comment = comment

            new_transaction_log = TransactionLog(
                user_id=user_id,
                action="Updated Content Review",
                content_id=content_id,
                timestamp=datetime.now(),
            )

            db.session.add(new_transaction_log)
            db.session.commit()
        else:
            rating = ContentReview(content_id=content_id, user_id=user_id, rating=rating_value, comment=comment)
            db.session.add(rating)

        db.session.commit()

        app.logger.info("Content Review Saved Successfully")
        return jsonify({'message': 'ContentReview saved successfully'}), 200
    except Exception as e:
        app.logger.info("Error Saving Content Review")
        return jsonify({'error': str(e)}), 500

# ROUTE - FETCH PREVIOUS RATING
@app.route('/get_previous_rating/<int:content_id>', methods=['GET'])
@jwt_required()
def get_previous_rating(content_id):
    try:
        user_id = get_jwt_identity()

        previous_rating = ContentReview.query.filter_by(content_id=content_id, user_id=user_id).first()

        if previous_rating:
            app.logger.info("Previous Rating Fetched")
            return jsonify({
                'rating': previous_rating.rating,
                'comment': previous_rating.comment
            }), 200
        else:
            app.logger.warn("No Previous Rating Found")
            return jsonify({
                'rating': None,
                'comment': None
            }), 200
    except Exception as e:
        app.logger.error("Error Fetching Previous User Rating")
        return jsonify({'error': str(e)}), 500
    
# ROUTE - Reader Count Per Section Graph
@app.route('/reader_count_per_section', methods=['GET'])
@jwt_required()
def reader_count_per_section():
    reader_counts_per_section = db.session.query(
        Section.name,
        func.count(distinct(User.id))
    ).join(Content, Content.section == Section.id).join(Borrowing, Borrowing.content_id == Content.id).join(User).filter(
        Borrowing.returned == False
    ).group_by(Section.name).all()

    section_names = [row[0] for row in reader_counts_per_section]
    reader_counts = [row[1] for row in reader_counts_per_section]

    plt.bar(section_names, reader_counts)
    plt.xlabel('Section')
    plt.ylabel('Reader Count')
    plt.title('Reader Count Per Section')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('reader_count_per_section.png')
    plt.close()

    app.logger.info("Section Based Reader Count Chart Fetched")
    return send_file('reader_count_per_section.png', mimetype='image/png')

# ROUTE - GENDER USER COUNT CHART 
@app.route('/user_count_gender', methods=['GET'])
@jwt_required()
def user_count_gender_chart():
    
    male_count = User.query.filter_by(gender='male').count()
    female_count = User.query.filter_by(gender='female').count()

    if np.isnan(male_count) or np.isnan(female_count):
        app.logger.warn("Invalid Data For Pie Chart")
        return "Error: Invalid data for pie chart"

    labels = ['Male', 'Female']
    counts = [male_count, female_count]

    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Male vs Female Users')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plt.clf()
    plt.close()

    app.logger.info("Gender Based Reader Count Chart Fetched")
    return send_file(buffer, mimetype='image/png')
    
# ROUTE - SEARCH BOOKS BY TITLE | SECTION | AUTHOR
@app.route('/search-result', methods=['GET'])
@jwt_required(optional=True)
def search_result():
    query = request.args.get('query')

    current_user_id = get_jwt_identity()

    content_results = Content.query.filter(Content.title.ilike(f'%{query}%')).all()

    formatted_content_results = []
    for content in content_results:
        image_data = content.image
        image_base64 = None
        if image_data:
            image_base64 = base64.b64encode(image_data).decode('utf-8')

        is_issued = False
        is_read = False
        is_requested = False
        is_wishlisted = False
        if current_user_id:
            borrowing = Borrowing.query.filter_by(content_id=content.id, member_id=current_user_id, returned=False).first()
            if borrowing:
                is_issued = True

            wishlist_item = Wishlist.query.filter_by(content_id=content.id, user_id=current_user_id).first()
            if wishlist_item:
                is_wishlisted = True

            read = Borrowing.query.filter_by(content_id=content.id, member_id=current_user_id, returned=False).first()
            if read:
                is_read = True

            issueRequest = IssueRequest.query.filter_by(contentId=content.id, userId=current_user_id, response='Pending').first()
            if issueRequest:
                is_requested = True

        result = {
            'id': content.id,
            'title': content.title,
            'author': content.author,
            'section': content.section,
            'rating': db.session.query(func.avg(ContentReview.rating)).filter(ContentReview.content_id == content.id).scalar(),
            'imageType': content.imageType,
            'image': image_base64,
            'isRead': is_read,
            'isIssued': is_issued,
            'isWishlisted': is_wishlisted,
            'isRequested': is_requested
        }

        formatted_content_results.append(result)

    app.logger.info("Search Result Fetched")
    return jsonify({'results': formatted_content_results})

# ROUTE - USER WISHLIST
@app.route('/wishlist/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_wishlist(user_id):
    try:
        current_user_id = get_jwt_identity()

        wishlist_items = Wishlist.query.filter_by(user_id=user_id).all()

        wishlist = []

        for item in wishlist_items:
            content = Content.query.get(item.content_id)

            image_data = content.image
            if image_data:
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            else:
                image_base64 = None

            is_read = False
            if current_user_id:
                borrowing = Borrowing.query.filter_by(content_id=content.id, member_id=current_user_id).first()
                if borrowing:
                    is_read = True

            is_wishlisted = False
            if current_user_id:
                wishlist_item = Wishlist.query.filter_by(user_id=current_user_id, content_id=content.id).first()
                if wishlist_item:
                    is_wishlisted = True

            is_issued = False
            if current_user_id:
                issued = Borrowing.query.filter_by(member_id=current_user_id, content_id=content.id, returned=False).first()
                if issued:
                    is_issued = True
            
            is_requested = False
            issueRequest = IssueRequest.query.filter_by(contentId=content.id, userId=current_user_id, response='Pending').first()
            if issueRequest:
                is_requested = True

            wishlist.append({
                'id': content.id,
                'title': content.title,
                'author': content.author,
                'image': image_base64,
                'number_of_pages': content.number_of_pages,
                'publish_year': content.publish_year,
                'isRead': is_read,
                'isIssued': is_issued,
                'isWishlisted': is_wishlisted,
                'isRequested': is_requested
            })

        app.logger.info("User Wishlist Fetched")
        return jsonify({'wishlist': wishlist}), 200
    except Exception as e:
        app.logger.error("Error Fetching User Wishlist", str(e))
        return jsonify({'error': str(e)}), 500
    
    
# ROUTE - USER DETAILS
@app.route('/user/<int:user_id>', methods=['GET'])
@cache.cached(timeout=60)
@jwt_required()
def get_user_details(user_id):
    try:
        user = User.query.get(user_id)

        if not user:
            app.logger.warn("No User Found For Fetching User Details")
            return jsonify({'error': 'User not found'}), 404

        user_details = {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'username': user.username,
            'phoneNumber': user.phoneNumber,
            'email': user.email,
            'gender': user.gender,
            'address': user.address,
            'city': user.city,
            'state': user.state,
            'zip': user.zip,
            'role': user.role
        }

        app.logger.info("User Details Fetched")
        return jsonify(user_details), 200
    except Exception as e:
        app.logger.error("Error Fetching User Details")
        return jsonify({'error': str(e)}), 500

def getUserFromToken(token):
    try:
        decoded_token = decode_token(token)
        user_id = decoded_token['identity']
        role = decoded_token['role']
        username = decoded_token['username']
        email = decoded_token['email']
        
        app.logger.info("User Fetched From -> Token Decoded")
        return {'id': user_id, 'role': role, 'username': username, 'email': email}
    except Exception as e:
        app.logger.error("Error Decoding Token", str(e))
        return None

# Create Issue Request
@app.route('/create_request/<int:contentId>', methods=['POST'])
@jwt_required()
def create_request(contentId):
    try:
        current_user_id = get_jwt_identity()
        
        # Check if an issue request for the given contentId and userId already exists
        existing_request = IssueRequest.query.filter(
        IssueRequest.contentId == contentId,
        IssueRequest.userId == current_user_id,
        IssueRequest.response != 'Accepted'
        ).first()
        
        if existing_request:
            app.logger.warn("Issue Request Already Present")
            return jsonify({'message': 'Issue request already exists'}), 400

        # Create the issue request in the database
        new_issue_request = IssueRequest(contentId=contentId, userId=current_user_id)
        db.session.add(new_issue_request)
        db.session.commit()
        
        app.logger.info("Issue Request Created")
        return jsonify({'message': 'Issue request created successfully'}), 201
    except Exception as e:
        app.logger.error("Error Creating Request")
        return jsonify({'error': str(e)}), 500
    
# Fetch Issue Request
@app.route('/fetch_issue_requests', methods=['GET'])
@jwt_required()
def get_issue_requests():
    try:
        issue_requests = IssueRequest.query.filter_by(response='Pending').all()
        app.logger.info("Issue Requests Fetched")
        return jsonify([{'contentId': ir.contentId, 'userId': ir.userId} for ir in issue_requests]), 200
    except Exception as e:
        app.logger.error("Error Fetching Issue Requests")
        return jsonify({'error': str(e)}), 500

# View Detail Request
@app.route('/detail_view/<int:content_id>/<int:user_id>', methods=["GET"])
@jwt_required()
def detailed_view(content_id, user_id):
    try:
        # Fetch user and content details using content_id and user_id
        user = User.query.get(user_id)
        content = Content.query.get(content_id)
        
        if user is None or content is None:
            return jsonify({'error': 'User or content not found'}), 404
        
        # Prepare response data
        response_data = {
            'username': user.username,
            'contentName': content.title,
            'sectionName': Section.query.get(content.section).name
        }
        
        app.logger.info("Details fetched successfully")
        return jsonify(response_data), 200
    except Exception as e:
        app.logger.error("Error fetching details: %s", str(e))
        return jsonify({'error': 'Error fetching details'}), 500    

# Reject Issue Request
@app.route("/reject_request/<int:content_id>/<int:user_id>", methods=["GET", "POST"])
@jwt_required()
def reject_request(content_id, user_id):
    try:
        issue_request = IssueRequest.query.filter_by(contentId=content_id, userId=user_id).first()
        if issue_request:
            issue_request.response = "Rejected"
            db.session.commit()
            return jsonify({"message": "Issue request rejected successfully"}), 200
        else:
            app.logger.warn("Issue Request not found for the specified content and user")
            return jsonify({"error": "Issue request not found"}), 404
    except Exception as e:
        app.logger.error("Error rejecting issue request", str(e))
        return jsonify({"error": "Rejecting issue request failed", "details": str(e)}), 500

# ROUTE - BUY OR DOWNLOAD CONTENT
@app.route('/download_purchase/<int:contentId>', methods=['GET'])
@jwt_required()
def download_purchase(contentId):

    current_user_id = get_jwt_identity()

    content = Content.query.get(contentId)
    if content is None:
        return abort(404, description="Content not found")

    content_amount = content.price

    pdf_blob = content.file

    pdf_bytes = BytesIO(pdf_blob)

    purchase_data = PurchaseData.query.filter_by(user_id=current_user_id, content_id=contentId).first()
    if purchase_data:

        new_transaction_log = TransactionLog(
            user_id=current_user_id,
            action="Re-Download",
            content_id=contentId,
            timestamp=datetime.now(),
        )

        db.session.add(new_transaction_log)

        db.session.commit()
        app.logger.info("PDF File Sent For Download - Already Paid")
        return send_file(pdf_bytes, as_attachment=True, mimetype='application/pdf', download_name="Book.pdf")
    
    if (purchase_data == None):
        user = User.query.get(current_user_id)
        if user.balance < content.price:
            app.logger.warn("Insufficient Account Balance")
            return abort(400, description="Insufficient balance to purchase content")

        user.balance -= content.price
        new_purchase = PurchaseData(user_id = current_user_id, content_id = contentId, amount=content_amount)
        db.session.add(new_purchase)
        db.session.commit()

        new_transaction_log = TransactionLog(
            user_id=current_user_id,
            action="Bought",
            content_id=contentId,
            timestamp=datetime.now(),
        )

        db.session.add(new_transaction_log)

        db.session.commit()

        app.logger.info("PDF File Sent For Download - Paid Now")
        return send_file(pdf_bytes, as_attachment=True, mimetype='application/pdf', download_name="Book.pdf")

    app.logger.error("Error Purchasing Content")
    return abort(403, description="Content not purchased")

# MAIN
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)