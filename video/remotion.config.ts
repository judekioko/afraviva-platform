import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
// Reuse the Django static assets (logo, hero video) via staticFile().
Config.setPublicDir('static');
