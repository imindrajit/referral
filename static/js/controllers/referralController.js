var app = angular.module("app");
app.controller("referralController", function($scope,referralAPIService){
        $scope.showError = 0;
        $scope.errorMessage = "";
        $scope.showSuccessMessage = 0;
        $scope.newUser = {
            'name': "",
            'email': "",
            'referred_by_code': ""
        };

        $scope.saveUser = function() {
            var saveUserApiCall = referralAPIService.saveUser($scope.newUser);
            saveUserApiCall.success(function(data,status){
                $scope.showError = 0;
                console.log("ho gya");
                console.log(status);
                console.log(data);
                $scope.showSuccessMessage = 1;
                $scope.userLink = '/user/' + data["user"]["id"];
                console.log($scope.userLink);
            });
            saveUserApiCall.error(function(data,status){
                $scope.showError = 1;
                $scope.showSuccessMessage = 0;
                $scope.errorMessage = data["message"];
                console.log(status);
                console.log(data);
            });
        };

        $scope.getUserData = function(id) {
            console.log(id);
            referralAPIService.getUser(id).success(function(data){
                console.log(data);
                var user_data=data["user"];
                $scope.user_data = {
                    "name": user_data["name"],
                    "email": user_data["email"],
                    "referral_score": user_data["referral_score"],
                    "wallet": user_data["wallet"]
                };
                if(data["referral_code"] == null)
                {
                    $scope.user_data["referral_code"] = "";
                }else{
                    $scope.user_data["referral_code"] = user_data["referral_code"];
                }
                if(data["referred_by"] == null)
                {
                    $scope.user_data["referred_by"] = "";
                }else{
                    $scope.user_data["referred_by"] = user_data["referred_by"];
                }
            });
        }
    }
);