'use strict';

var yaiaHeader = angular.module('yaia.header', []);

yaiaHeader.controller('HeaderCtrl', ['$scope', '$location', function($scope, $location) {
    $scope.isActive = function (viewLocation) { 
        return viewLocation === $location.path();
    };
}]);
