var app = angular.module("app");
app.factory("couponAPIService", function ($http) {
    var couponAPI = {};

    couponAPI.generateCouponCode = function (coupon) {
        return $http.post('/api/v1/user/generate-coupon-code/', coupon);
    };

    couponAPI.redeemCode = function (couponUser) {
        return $http.post('/api/v1/user/redeem-code/', couponUser);
    };

    return couponAPI;
});