import Vue from "vue";
import Vuex from "vuex";
import pers from "vuex-persistedstate";

Vue.use(Vuex);

export default new Vuex.Store({
  plugins: [
    pers({
      storage: window.localStorage,
    }),
  ],
  state: {
    user: {},
    access_token: "",
  },
  mutations: {},
  actions: {},
  modules: {},
});
