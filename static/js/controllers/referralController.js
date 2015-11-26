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
            referralAPIService.getUser(id).success(function(data,status){
                $scope.user=data;
                console.log(data);
            });
        }
    }
);