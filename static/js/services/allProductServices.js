var app = angular.module("app");
app.factory("allProductsAPIService", function ($http) {
    var allProductsAPI = {};
    allProductsAPI.getAllProducts = function () {
        return $http({
            method: 'GET',
            url: '/api/products'
        });
    };

    return allProductsAPI;
});