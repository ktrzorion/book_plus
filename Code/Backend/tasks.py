from flask import jsonify
import celery
from flask_mail import Message
from datetime import datetime, timedelta
from app import mail
from models import db, User, ContentReview, Borrowing, LoginData, Content, IssueRequest
from reportlab.pdfgen import canvas 
from io import BytesIO
import logging

@celery.shared_task(name="send_email")
def desert_user():
    threshold_time = datetime.now() - timedelta(days=1)
    # Query to retrieve inactive users
    inactive_users = User.query.join(LoginData).filter(LoginData.last_login_time < threshold_time).all()
    print(inactive_users)

    # Send email to each inactive user
    for user in inactive_users:
        # Customize your email content and subject
        subject = 'Reminder: Log in to our Library Management System'
        body = f'Dear {user.firstname},\n\nThis is a reminder to log in to our Library Management System.'
        sender = "noreply@app.com"
        # Create and send the email
        print(user.email)
        msg = Message(subject, sender=sender, recipients=[user.email], body=body)

        try:
            mail.send(msg)
            return "Email Sent"
        except Exception as e:
            print(e)
            
            return f"Failed Sending Email {e}"
        
@celery.shared_task(name="monthly_report")
def monthly_report():
    try:
        # Get all users
        all_users = User.query.all()

        # Loop through each user
        for user in all_users:
            # Query necessary data related to the user
            active_borrowings_count = Borrowing.query.filter_by(member_id=user.id, returned=False).count()
            wishlist_items_count = len(user.wishlist_items)

            # Generate PDF report
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer)
            c.drawString(100, 750, "Monthly Report for User: {}".format(user.username))
            c.drawString(100, 730, "Active Borrowings: {}".format(active_borrowings_count))
            c.drawString(100, 710, "Wishlist Items Count: {}".format(wishlist_items_count))
            c.save()

            sender = "noreply@app.com"

            # Send email with PDF report
            msg = Message("Monthly Report", sender=sender, recipients=[user.email])
            msg.body = "Please find attached the monthly report."
            msg.attach("monthly_report.pdf", "application/pdf", pdf_buffer.getvalue())
            mail.send(msg)

        return jsonify({"message": "Monthly reports sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to generate monthly reports", "details": str(e)}), 500

@celery.shared_task(name="revoke_access")
def revoke_access():

    # Get all borrowings where the last_return_date is before the current date
    expired_borrowings = Borrowing.query.filter(Borrowing.last_return_date < datetime.now()).all()
    print(datetime.now(), expired_borrowings)

    for borrowing in expired_borrowings:
        print(borrowing.last_return_date)
        borrowing.returned = True
        borrowing.return_date = datetime.now()
        borrowing.is_read = True

    # Commit changes to the database
    db.session.commit()

    print("Borrowings updated successfully")

@celery.shared_task(name="delete_rejected_issue_requests")
def delete_rejected_issue_requests():
    try:
        # Query all IssueRequest instances with response set to "REJECTED"
        rejected_issue_requests = IssueRequest.query.filter_by(response="Rejected").all()

        # Delete each rejected issue request
        for issue_request in rejected_issue_requests:
            db.session.delete(issue_request)

        # Commit the changes to the database
        db.session.commit()

        return {"message": "Rejected issue requests deleted successfully"}, 200
    except Exception as e:
        return {"error": "Failed to delete rejected issue requests", "details": str(e)}, 500