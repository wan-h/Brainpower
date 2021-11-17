const path = require('path');
const yaml = require('yamljs')
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { clear } = require('console');

module.exports = {
    // 三种模式：development, production 或 none，设置mode参数启动webpack 内置在相应环境下的优化
    mode: 'development',
    // 入口起点，指示webpack应该使用哪个模块，作为构建其内部依赖图
    // entry: '/src/index.js',
    entry: {
        index: './src/index.js',
        print: './src/print.js',
    },
    output: {
        // 主要输出文件为main.js, 对应entry
        // filename: 'main.js',
        // filename: 'bundle.js',
        filename: '[name].bundle.js',
        // 其他生成文件放在./dist文件下
        path: path.resolve(__dirname, 'dist'),
        // 执行npm build之后会删除之前构建生成的文件
        clean: true,
    },
    // 增强调试过程
    // inline-source-map帮助追踪到具体的js,webpack打包后被指定到bundle.js
    devtool: 'inline-source-map',
    // 告知 webpack-dev-server，将 dist 目录下的文件 serve 到 localhost:8080 下，配合webpack serve --open修改代码后实时刷新前端页面
    devServer: {
        static: './dist'
    },
    // webpack 只能理解 JavaScript 和 JSON 文件，这是 webpack 开箱可用的自带能力
    // loader 让 webpack 能够去处理其他类型的文件，并将它们转换为有效 模块，以供应用程序使用，以及被添加到依赖图中
    module: {
        rules: [
            {
                // 识别出哪些文件会被转换
                test: /\.css$/i,
                // 定义出在进行转换时，应该使用哪个 loader
                // 第一个 loader 将其结果（被转换后的资源）传递给下一个 loader，依此类推。最后，webpack 期望链中的最后的 loader 返回 JavaScript
                use: ['style-loader', 'css-loader'],
            },
            {
                // 加载图片
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                type: 'asset/resource',
            },
            {
                // 加载字体
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                type: 'asset/resource',
            },
            // 加载数据文件
            {
                test: /\.(csv|tsv)$/i,
                use: ['csv-loader'],
            },
            {
                test: /\.xml$/i,
                use: ['xml-loader'],
            },
            // 自动以parser替代特定的webpack loader
            {
                test: /\.yaml$/i,
                type: 'json',
                parser: {
                  parse: yaml.parse,
                },
            },
        ],
    },
    // loader 用于转换某些类型的模块，而插件则可以用于执行范围更广的任务。包括：打包优化，资源管理，注入环境变量。
    plugins: [
        // 将html自动转到生成到输出中（正常graph是追踪不到html文件的，因为不被任何js依赖）
        new HtmlWebpackPlugin({
            title: 'quickStart'
        }),
    ],
};

// 使用配置文件
// npx webpack --config webpack.config.js
// 
// package.json中增加script: "build": "webpack" 后直接使用npm run build