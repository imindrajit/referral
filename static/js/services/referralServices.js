var app = angular.module("app");
app.factory("referralAPIService", function ($http) {
    var referralAPI = {};

    referralAPI.saveUser = function (user) {
        return $http.post('/api/v1/user/', user);
    };

    referralAPI.getUser = function (id) {
        return $http.get('/api/v1/user/' + id);
    };

    referralAPI.generateReferralCode = function (rcodeUser) {
        return $http.post('/api/v1/user/generate-referral-code/', rcodeUser);
    };

    referralAPI.getAllUsers = function() {
        return $http.get('/api/v1/users/');
    };

    return referralAPI;
});