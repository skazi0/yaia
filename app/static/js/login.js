'use strict';

var yaiaLogin = angular.module('yaia.login', ['ui.router', 'yaia.auth']);

yaiaLogin.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('anon.login', {url: '/login', templateUrl: 'static/views/partials/login.html', controller: 'LoginCtrl', resolve: { $title: function() { return 'Sign In'; }}});
}]);

yaiaLogin.controller('LoginCtrl', ['$scope', '$state', 'Auth', function($scope, $state, Auth) {
    $scope.waiting = false;

    $scope.signin = function() {
        $scope.waiting = true;
        Auth.login($scope.login, $scope.password, $scope.remember).then(
            function(){
                $state.go(Auth.targetState ? Auth.targetState : 'user.home', Auth.targetStateParams);
                $scope.waiting = false;
            },
            function(){
                $scope.waiting = false;
                alert('login failed');                
            }
        );
    };
}]);
