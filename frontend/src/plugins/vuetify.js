import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import de from 'vuetify/lib/locale/de';

import '@fortawesome/fontawesome-pro/css/all.css'

Vue.use(Vuetify);


// https://coolors.co/8ecae6-219ebc-023047-ffb703-fb8500
// https://coolors.co/f8ffe5-06d6a0-1b9aaa-ef476f-ffc43d

export default new Vuetify({
  theme: {
      options: {
        customProperties: true,
      },
    themes: {
      light: {
          primary: '#023047',          
          secondary: '#219ebc',
          accent: '#82B1FF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#fb8500',
          oecheryellow: "ffc43d"
      },
    },
  },
    lang: {
      locales: { de },
      current: 'de',
    },
  icons: {
    iconfont: 'fa',
  },
});
