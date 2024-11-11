let appPackageName = 'backend';
let filePath = '';

//importScripts('js/service-worker/cache-polyfill.js');

/*
 *
 *  Air Horner
 *  Copyright 2015 Google Inc. All rights reserved.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License
 *
 */
if (!Cache.prototype.add) {
    Cache.prototype.add = function add(request) {
        return this.addAll([request]);
    };
}

if (!Cache.prototype.addAll) {
    Cache.prototype.addAll = function addAll(requests) {
        var cache = this;

        // Since DOMExceptions are not constructable:
        function NetworkError(message) {
            this.name = 'NetworkError';
            this.code = 19;
            this.message = message;
        }

        NetworkError.prototype = Object.create(Error.prototype);

        return Promise.resolve().then(function () {
            if (arguments.length < 1) throw new TypeError();

            // Simulate sequence<(Request or USVString)> binding:
            var sequence = [];

            requests = requests.map(function (request) {
                if (request instanceof Request) {
                    return request;
                }
                else {
                    return String(request); // may throw TypeError
                }
            });

            return Promise.all(
                requests.map(function (request) {
                    if (typeof request === 'string') {
                        request = new Request(request);
                    }

                    var scheme = new URL(request.url).protocol;

                    if (scheme !== 'http:' && scheme !== 'https:') {
                        throw new NetworkError("Invalid scheme");
                    }

                    return fetch(request.clone());
                })
            );
        }).then(function (responses) {
            // TODO: check that requests don't overwrite one another
            // (don't think this is possible to polyfill due to opaque responses)
            return Promise.all(
                responses.map(function (response, i) {
                    return cache.put(requests[i], response);
                })
            );
        }).then(function () {
            return undefined;
        });
    };
}

if (!CacheStorage.prototype.match) {
    // This is probably vulnerable to race conditions (removing caches etc)
    CacheStorage.prototype.match = function match(request, opts) {
        var caches = this;

        return this.keys().then(function (cacheNames) {
            var match;

            return cacheNames.reduce(function (chain, cacheName) {
                return chain.then(function () {
                    return match || caches.open(cacheName).then(function (cache) {
                        return cache.match(request, opts);
                    }).then(function (response) {
                        match = response;
                        return match;
                    });
                });
            }, Promise.resolve());
        });
    };
}

self.addEventListener('install', function (e) {

    e.waitUntil(
        caches.open(appPackageName).then(function (cache) {

            return cache.addAll([

                filePath

            ]);

        })
    );

});

self.addEventListener('fetch', function (event) {

    event.respondWith(
        caches.match(event.request).then(function (response) {

            //return response || fetch(event.request);

            // Cache hit - return response
            if (response) {
                return response;
            }

            return fetch(event.request);

            // IMPORTANT: Clone the request. A request is a stream and
            // can only be consumed once. Since we are consuming this
            // once by cache and once by the browser for fetch, we need
            // to clone the response.
            // var fetchRequest = event.request.clone();
            //
            // return fetch(fetchRequest).then(
            //     function(response) {
            //         // Check if we received a valid response
            //         if(!response || response.status !== 200 || response.type !== 'basic') {
            //             return response;
            //         }
            //
            //         // IMPORTANT: Clone the response. A response is a stream
            //         // and because we want the browser to consume the response
            //         // as well as the cache consuming the response, we need
            //         // to clone it so we have two streams.
            //         var responseToCache = response.clone();
            //
            //         caches.open(appPackageName)
            //             .then(function(cache) {
            //                 cache.put(event.request, responseToCache);
            //             });
            //
            //         return response;
            //     }
            // );

        })
    );

});

