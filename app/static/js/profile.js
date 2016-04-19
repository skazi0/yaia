'use strict';

var yaiaProfile = angular.module('yaia.profile', ['ui.router']);

yaiaProfile.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('user.profile', {url: '/profile', templateUrl: 'static/views/partials/profile.html', controller: 'ProfileCtrl', resolve: { $title: function() { return 'Profile'; }}});
}]);

yaiaProfile.controller('ProfileCtrl', ['$scope', function($scope) {
    $scope.todo = 'profile information and settings';
}]);
