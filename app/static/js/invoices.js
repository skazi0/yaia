'use strict';

var yaiaInvoices = angular.module('yaia.invoices', ['ui.router', 'ui.select', 'ngSanitize', 'angular-collapse', 'restangular', 'ngTable']);

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

yaiaInvoices.controller('InvoiceCtrl', ['$scope', '$sce', '$state', '$stateParams', 'Invoices', 'Customers', 'Restangular', function($scope, $sce, $state, $stateParams, Invoices, Customers, Restangular) {
    $scope.id = $stateParams.id;
    $scope.selectedCustomer = {};
    $scope.loadCustomers = function() {
        Customers.getList().then(
            function(data) {
                $scope.customers = data;
            }
        );
    };
    $scope.trustAsHtml = function(value) {
      return $sce.trustAsHtml(value);
    };
    $scope.fillCustomer = function(item, model) {
        if (!item)
            return;
        Customers.one(item.id).get().then(
            function(data) {
                data = Restangular.stripRestangular(data);
                for (var prop in data) {
                    $scope.invoice['customer_' + prop] = data[prop];
                }
              $scope.selectedCustomer.item = null;
            }
        );
        $scope.customerSelectOpen = false;
    };
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
                $scope.title = 'Edit Invoice #' + data.ref_num;
                $scope.invoice = data;
            }
        );
    }
}]);
