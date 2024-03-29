const BundleTracker = require("webpack-bundle-tracker");
const BundleAnalyzerPlugin = require("webpack-bundle-analyzer").BundleAnalyzerPlugin;


const pages = {
    main: {
        entry: './src/main.js',
        chunks: ['chunk-vendors']
    },
    vignette: {
        entry: './src/vignette.js',
        chunks: ['chunk-vendors']
    },   
     instructions: {
        entry: './src/components/InstructionManager/instruction_manager.js',
        chunks: ['chunk-vendors']
    },
    no_chat: {
        entry: './src/no_chat.js',
        chunks: ['chunk-vendors']
    },
    instruction_bar: {
        entry: './src/instruction_bar.js',
        chunks: ['chunk-vendors']
    },
    essay: {
        entry: './src/components/Essay/essay.js',
        chunks: ['chunk-vendors']
    },

};

module.exports = {

    runtimeCompiler: true,
    "transpileDependencies": [
        "vuetify"
    ],
    pages: pages,
    filenameHashing: false,
    productionSourceMap: false,
    publicPath: process.env.NODE_ENV === 'production'
        ? '/static/vue'
        : 'http://localhost:8080/',
    outputDir: '../_static/vue/',

    chainWebpack: config => {
        config.optimization
            .splitChunks({
                cacheGroups: {
                    moment: {
                        test: /[\\/]node_modules[\\/]moment/,
                        name: "chunk-moment",
                        chunks: "all",
                        priority: 5
                    },
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: "chunk-vendors",
                        chunks: "all",
                        priority: 1
                    },
                },
            });

        // Object.keys(pages).forEach(page => {
        //     config.plugins.delete(`html-${page}`);
        //     config.plugins.delete(`preload-${page}`);
        //     config.plugins.delete(`prefetch-${page}`);
        // })

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{ filename: './webpack-stats.json' }]);

        // Uncomment below to analyze bundle sizes
        // config.plugin("BundleAnalyzerPlugin").use(BundleAnalyzerPlugin);

        config.resolve.alias
            .set('__STATIC__', 'static');

        config.devServer
            .public('http://localhost:8080')
            .host('localhost')
            .port(8080)
            .hotOnly(true)
            .watchOptions({ poll: 1000 })
            .https(false)
            .headers({ "Access-Control-Allow-Origin": ["*"] });
        config.module.rules.delete('eslint');

    }
};