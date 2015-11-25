var app = angular.module("app");
app.controller("referralController", function($scope,referralAPIService){

        $scope.newUser = {
            'name': "",
            'email': "",
            'referred_by_code': ""
        };
        $scope.saveUser = function() {
            var saveUserApiCall = referralAPIService.saveUser($scope.newUser);
            saveUserApiCall.success(function(data,status,headers,response){
                if(response)
                {
                    console.log("ho gya");
                }else{
                    console.log("nahi hua");
                }
                console.log(status);
            });
            saveUserApiCall.error(function(data,status,headers,response){
                console.log(status);
            });
        };
    }
);