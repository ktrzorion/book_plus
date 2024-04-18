import { createRouter, createWebHashHistory } from 'vue-router'
import AboutUs from '../components/AboutUs.vue'
import ReaderHome from '../components/ReaderHome.vue'
import LibrarianHome from '../components/LibrarianHome.vue'
import AddBook from '../components/AddBook'
import BorrowBook from '../components/BorrowBook'
import CreateSection from '../components/CreateSection'
import LoginPage from '../components/LoginPage'
import RegistrationPage from '../components/RegistrationPage'
import SearchResult from '../components/SearchResult'
import TransactionLogs from '../components/TransactionLogs'
import UpdateContent from '../components/UpdateContent'
import UpdateSection from '../components/UpdateSection'
import UploadContent from '../components/UploadContent'
import HomePage from '../components/HomePage'
import UserProfile from '../components/UserProfile'
import ReaderWishlist from '../components/ReaderWishlist'
import RateContent from '../components/RateContent'
import SummaryGraph from '../components/SummaryGraph.vue'
import ActivityPage from '../components/ActivityPage.vue'
import RequestList from '@/components/RequestList.vue'
import DetailView from '@/components/DetailView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/userprofile/:userId',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true }
  },
  {
    path: '/rate/:contentId',
    name: 'RateContent',
    component: RateContent,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/wishlist/:userId',
    name: 'ReaderWishlist',
    component: ReaderWishlist,
    meta: { requiresAuth: true }
  },
  {
    path: '/reader-home',
    name: 'ReaderHome',
    component: ReaderHome,
    meta: { requiresAuth: true }
  },
  {
    path: '/detail_view/:contentId/:userId',
    name: 'DetailView',
    component: DetailView,
    meta: { requiresAuth: true }
  },
  {
    path: '/librarian-home',
    name: 'LibrarianHome',
    component: LibrarianHome,
    meta: { requiresAuth: true }
  },
  {
    path: '/about',
    name: 'AboutUs',
    component: AboutUs
  },
  {
    path: '/addbook',
    name: 'AddBook',
    component: AddBook,
    meta: { requiresAuth: true }
  },
  {
    path: '/borrowbook',
    name: 'BorrowBook',
    component: BorrowBook,
    meta: { requiresAuth: true }
  },
  {
    path: '/activity-page/:contentId',
    name: 'ActivityPage',
    component: ActivityPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/request-list',
    name: 'RequestList',
    component: RequestList,
    meta: {requiresAuth: true }
  },
  {
    path: '/createcategory',
    name: 'CreateCategory',
    component: CreateSection,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/register',
    name: 'RegistrationPage',
    component: RegistrationPage
  },
  {
    path: '/searchresult/:query',
    name: 'searchResult',
    component: SearchResult
  },
  {
    path: '/transactionlogs',
    name: 'TransactionLogs',
    component: TransactionLogs,
    meta: { requiresAuth: true }
  },
  {
    path: '/update-content/:contentId',
    name: 'UpdateContent',
    component: UpdateContent,
    meta: { requiresAuth: true }
  },
  {
    path: '/update-section/:sectionId',
    name: 'UpdateSection',
    component: UpdateSection,
    meta: { requiresAuth: true }
  },
  {
    path: '/upload-content/:sectionId',
    name: 'UploadContent',
    component: UploadContent,
    meta: { requiresAuth: true }
  },
  {
    path: '/create-section',
    name: 'CreateSection',
    component: CreateSection,
    meta: { requiresAuth: true }
  },
  {
    path: '/summary-graph',
    name: 'SummaryGraph',
    component: SummaryGraph,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    checkAuthentication(to, next);
  } else {
    next();
  }
});

function checkAuthentication(to, next) {
  const token = sessionStorage.getItem('token');
  if (!token) {
    console.log('Token not found in session storage. User is not authenticated.');
    // Check if already navigating to the login page to avoid infinite loop
    if (to.name !== 'LoginPage') {
      // Redirect to login page with attempted URL stored in query parameters
      next({ path: '/login', query: { redirect: to ? to.fullPath : '/' } });
    } else {
      // If already navigating to login page, allow navigation to continue
      next();
    }
    return;
  }

  try {
    fetch('http://127.0.0.1:5000/verify', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data.authenticated) {
        console.log('User is authenticated:', data.user.username);
        // Allow navigation to continue
        next();
      } else {
        console.log('User is not authenticated.');
        // Redirect to login page with attempted URL stored in query parameters
        next({ path: '/login', query: { redirect: to ? to.fullPath : '/' } });
      }
    })
    .catch(error => {
      console.error('Error checking login status:', error);
      // Redirect to login page with attempted URL stored in query parameters
      next({ path: '/login', query: { redirect: to ? to.fullPath : '/' } });
    });
  } catch (error) {
    console.error('Error checking login status:', error);
    // Redirect to login page with attempted URL stored in query parameters
    next({ path: '/login', query: { redirect: to ? to.fullPath : '/' } });
  }
}

export default router