'use strict';

var yaiaInvoices = angular.module('yaia.invoices', ['ui.router', 'ui.select', 'ngSanitize', 'angular-collapse', 'restangular', 'ngTable', 'ngFileSaver']);

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

yaiaInvoices.factory('Calculator', ['Restangular', function (Restangular) {
    return Restangular.service('calculator');
}]);

yaiaInvoices.factory('Exporter', ['Restangular', function (Restangular) {
    return Restangular.withConfig(function(config) {
        config.setFullResponse(true);
    }).service('export');
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

yaiaInvoices.controller('InvoiceCtrl', ['$scope', '$sce', '$state', '$stateParams', 'Invoices', 'Calculator', 'Exporter', 'Customers', 'Restangular', 'NgTableParams', 'FileSaver', 'Blob', function($scope, $sce, $state, $stateParams, Invoices, Calculator, Exporter, Customers, Restangular, NgTableParams, FileSaver, Blob) {
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
    $scope.lineEditStart = function(row, rowForm) {
        row.org = angular.copy(row);
        row.isEditing = true;
    };
    $scope.lineEditCancel = function(row, rowForm) {
        angular.extend(row, row.org);
        delete row.org;
        row.isEditing = false;
    };
    $scope.lineEditSave = function(row) {
        delete row.org;
        row.isEditing = false;
        row.isCalculating = true;
        Calculator.post($scope.invoice).then(
            function(data) {
                angular.forEach($scope.invoice.lines, function(line, index) {
                    line.net_value = data.lines[index].net_value;
                    delete line.isCalculating;
                });
            },
            function(resp) {
                alert("ERROR");
            }
        );
    };
    $scope.lineDelete = function(row) {
        alert("delete" + row);
    };
    $scope.export = function() {
        function extractFilename(headers) {
            var value = headers['content-disposition'];
            value = value.split(';')[1].trim().split('=')[1];
            return value.replace(/"/g, ''); // " coloring fix
        };
        Exporter.post($scope.invoice).then(
            function(resp) {
                var headers = resp.headers();
                var bdata = new Blob([resp.data], { type: headers['content-type'] });
                FileSaver.saveAs(bdata, extractFilename(headers));
            },
            function(resp) {
                alert("ERROR");
            }
        );
    };
    //
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
                $scope.tableParams = new NgTableParams(
                    {
                        count: data.length, // disable paging
                    },
                    {
                        counts: [], // disable page sizes display
                        data: data.lines,
                    }
                );
            }
        );
    }
}]);
