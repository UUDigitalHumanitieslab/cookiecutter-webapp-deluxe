import { history } from 'backbone';
import { when, ready } from 'jquery';
import '@dhl-uu/jquery-promise';

import * as config from 'config.json';
import { i18nPromise } from './global/i18n';
import './global/internalLinks';
import './global/hbsHelpers';
import './aspects/example';

when(ready, i18nPromise).done(function() {
    let success = history.start({
        root: config.baseUrl,
        pushState: true,
    });
});
