import { createStore } from 'vuex';

export default new createStore({
  state: {
    alert: {
      show: false,
      type: 'alert-success',
      message: '',
    },
  },
  mutations: {
    showAlert(state, { message, type }) {
      state.alert.message = message;
      state.alert.type = type;
      state.alert.show = true;

      setTimeout(() => {
        state.alert.show = false;
      }, 3000);
    },
  },
  actions: {
  },
  getters: {
    alert(state) {
      return state.alert;
    },
  },
});