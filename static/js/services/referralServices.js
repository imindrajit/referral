var app = angular.module("app");
app.factory("referralAPIService", function ($http) {
    var referralAPI = {};

    referralAPI.saveUser = function (user) {
        return $http.post('/api/v1/user/', user);
    };

    return referralAPI;
});