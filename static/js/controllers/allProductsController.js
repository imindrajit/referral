var app = angular.module("app");
    app.controller("allProductsController", function($scope,allProductsAPIService){

        $scope.allProducts = function() {
            allProductsAPIService.getAllProducts().success(function (response){
                $scope.products = response;
            });
        };
    }
);