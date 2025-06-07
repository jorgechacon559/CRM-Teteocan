import api from "../axios";

export default {

    login(credentials) {
        return api.post('/usuarios/login', credentials);
    },

    register(credentials) {
        return api.post('/usuarios/registrar', credentials);
    }
}