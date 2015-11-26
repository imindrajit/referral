var app = angular.module("app");
app.factory("referralAPIService", function ($http) {
    var referralAPI = {};

    referralAPI.saveUser = function (user) {
        return $http.post('/api/v1/user/', user);
    };

    referralAPI.getUser = function (id) {
        return $http.get('/api/v1/user/' + id);
    };

    return referralAPI;
});