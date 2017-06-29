
'use strict';

export function loadScript (url, async) {
  return new Promise(function (resolve, reject) {
    var script = document.createElement('script');
    script.src = url;
    if (typeof async !== 'undefined') {
      script.async = async;
    }

    script.onerror = reject;
    script.onload = resolve;
    document.head.appendChild(script);
  });
}

export function loadStyles (url) {
  return new Promise(function (resolve, reject) {
    var xhr = new XMLHttpRequest();
    xhr.returnType = 'text';
    xhr.onload = function () {
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = url;
      document.head.appendChild(link);
      resolve();
    };
    xhr.onerror = reject;
    xhr.open('get', url);
    xhr.send();
  });
}
