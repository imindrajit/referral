var app = angular.module("app");
app.controller("couponController", function($scope,couponAPIService) {
    $scope.coupon = {
        'value': "",
        'code': "",
        'use_limit': ""
    };
    $scope.couponUser = {
        'email': "",
        'code': ""
    };
    $scope.showError = 0;
    $scope.showSuccessMessage = 0;
    $scope.errorMessage = "";

    $scope.generateCouponCode = function() {
        console.log($scope.coupon);
        var generateCode = couponAPIService.generateCouponCode($scope.coupon);
        generateCode.success(function (data,status) {
            $scope.showError = 0;
            console.log(status);
            console.log(data);
            $scope.showSuccessMessage = 1;
            $scope.coupon["value"] = data["coupon"]["value"];
            $scope.coupon["use_limit"] = data["coupon"]["use_limit"];
            $scope.coupon["code"] = data["coupon"]["coupon_code"];
        });
        generateCode.error(function (data,status) {
            $scope.showError = 1;
            $scope.showSuccessMessage = 0;
            $scope.errorMessage = data["message"];
            console.log(status);
            console.log(data);
        });
    };

    $scope.redeemCode = function() {
        console.log($scope.couponUser);
        var redeemCode = couponAPIService.redeemCode($scope.couponUser);
        redeemCode.success(function (data, status) {
            $scope.showError = 0;
            console.log(status);
            console.log(data);
            $scope.showSuccessMessage = 1;
            $scope.couponUser["email"] = data["couponUser"]["email"];
            $scope.couponUser["code"] = data["couponUser"]["code"];
        });
        redeemCode.error(function (data,status) {
            $scope.showError = 1;
            $scope.showSuccessMessage = 0;
            $scope.errorMessage = data["message"];
            console.log(status);
            console.log(data);
        });
    };
});
