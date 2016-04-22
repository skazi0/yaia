'use strict';

var yaiaInvoices = angular.module('yaia.invoices', ['ui.router', 'restangular', 'ngTable']);

yaiaInvoices.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('user.invoices', {
        url: '/invoices/:id',
        templateUrl: function ($stateParams) { return 'static/views/partials/' + ($stateParams.id ? 'invoice.html' : 'invoices.html'); },
        controllerProvider: function ($stateParams) { return $stateParams.id ? 'InvoiceCtrl' : 'InvoicesCtrl'; },
        resolve: { $title: function() { return 'Invoices'; }}});
}]);

yaiaInvoices.factory('Invoices', ['Restangular', function (Restangular) {
    return Restangular.service('invoices');
}]);

yaiaInvoices.controller('InvoicesCtrl', ['$scope', 'Invoices', 'NgTableParams', function($scope, Invoices, NgTableParams) {
    $scope.tableParams = new NgTableParams(
        {
            count: 10,
            sorting: { issued_on: 'desc' },
        },
        {
            counts: [10, 20, 50, 100],
            getData: function(params) {
                var urlparams = params.url();
                // pass sorting as json for easier handling in backend
                urlparams.sorting = params.sorting();
                return Invoices.one().get(urlparams).then(
                    function(data) {
                        params.total(data.totalItemCount);
                        return data.items;
                    }
                );
            },
        }
    );
}]);

yaiaInvoices.controller('InvoiceCtrl', ['$scope', '$state', '$stateParams', 'Invoices', function($scope, $state, $stateParams, Invoices) {
    $scope.id = $stateParams.id;
    if ($scope.id == 'new') {
        $scope.title = 'New Invoice';
        $scope.invoice = {};
        $scope.save = function() {
            Invoices.post($scope.invoice).then(
                function(data) {
                    $state.go('user.invoices', {id: null});
                },
                function(resp) {
                    alert("ERROR");
                }
            );
        };
    } else {
        $scope.title = 'Edit Invoice';
        $scope.remove = function() {
            $scope.invoice.remove().then(
                function(data) {
                    $state.go('user.invoices', {id: null});
                },
                function(resp) {
                    alert("ERROR");
                }
            );
        };
        $scope.save = function() {
            $scope.invoice.put().then(
                function(data) {
                    $state.go('user.invoices', {id: null});
                },
                function(resp) {
                    alert("ERROR");
                }
            );
        };
        Invoices.one($scope.id).get().then(
            function(data) {
                $scope.invoice = data;
            }
        );
    }
}]);
