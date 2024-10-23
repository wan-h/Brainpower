/* eslint no-console:0 consistent-return:0 */
"use strict";

// 创建着色器，参数：gl上下文，着色器类型，着色器代码
function createShader(gl, type, source) {
  // 根据类型创建着色器对象，类型包含：顶点着色器、片段着色器
  var shader = gl.createShader(type);
  // 提供源代码
  gl.shaderSource(shader, source);
  // 编译 -> 生成着色器（这里之所有要编译是因为这里本质是一个异构系统，我们的着色器源代码需要到GPU上去运行）
  gl.compileShader(shader);
  // 校验编译是否成功
  var success = gl.getShaderParameter(shader, gl.COMPILE_STATUS);
  if (success) {
    return shader;
  }
  // 如果编译失败，打印错误信息并删除着色器对象
  console.log(gl.getShaderInfoLog(shader));
  gl.deleteShader(shader);
}

// 创建着色器程序，参数：gl上下文，顶点着色器，片段着色器
function createProgram(gl, vertexShader, fragmentShader) {
  var program = gl.createProgram();
  // 将着色器对象附加到程序对象上（这里就相当于编译一个可执行程序，将之前编译的着色器当作编译的依赖）
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  // 链接程序对象（这里就相当于我们为可执行程序添加链接库，链接的就是之前编译的着色器）
  gl.linkProgram(program);
  var success = gl.getProgramParameter(program, gl.LINK_STATUS);
  if (success) {
    return program;
  }

  console.log(gl.getProgramInfoLog(program));
  gl.deleteProgram(program);
}

function main() {
  // 找到canvas元素
  var canvas = document.querySelector("#myCanvas");
  // 获取webgl上下文（webgl上下文只存在于canvas中）
  var gl = canvas.getContext("webgl");
  if (!gl) {
    console.log("Unable to initialize WebGL. Your browser or machine may not support it.");
    return;
  }

  // 顶点着色器源码
  var vertexShaderSource = `
  // an attribute will receive data from a buffer
  attribute vec4 a_position;

  // all shaders have a main function
  void main() {

    // gl_Position is a special variable a vertex shader
    // is responsible for setting
    gl_Position = a_position;
  }
  `;
  // 片段着色器源码
  var fragmentShaderSource = `
  // fragment shaders don't have a default precision so we need
  // to pick one. mediump is a good default
  precision mediump float;

  void main() {
    // gl_FragColor is a special variable a fragment shader
    // is responsible for setting
    gl_FragColor = vec4(1, 0, 0.5, 1); // return redish-purple
  }
  `;

  // create GLSL shaders, upload the GLSL source, compile the shaders
  var vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
  var fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

  // Link the two shaders into a program
  var program = createProgram(gl, vertexShader, fragmentShader);

  // look up where the vertex data needs to go.
  // 这里的属性对应于顶点着色器中的a_position
  var positionAttributeLocation = gl.getAttribLocation(program, "a_position");

  // Create a buffer and put three 2d clip space points in it
  // 创建缓冲区对象（a_position是一个attribute，他只能从缓冲区中拿数据，所以需要创建一个缓冲区，然后填充发送给GPU的数据）
  var positionBuffer = gl.createBuffer();

  // Bind it to ARRAY_BUFFER (think of it as ARRAY_BUFFER = positionBuffer)
  // 这里就是申明了使用positionBuffer这个缓冲区（可以通过绑定点操控全局范围内的许多数据，当前绑定的就是这个）
  // ARRAY_BUFFER相当于一种指定，当前指向的就是positionBuffer
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

  /*
   * 顶点着色器中的gl_Position的坐标范围是[-1, 1]，所以这里需要将坐标映射到这个范围中
   * 裁剪空间         屏幕空间
   * 0, 0       ->   200, 150
   * 0, 0.5     ->   200, 225
   * 0.7, 0     ->   340, 150
   */
  var positions = [
    0, 0,
    0, 0.5,
    0.7, 0,
  ];
  // 将数据发送到缓冲区中
  // Float32Array是因为底层都是需要强类型的数据的，所以这里定义32位浮点型数据序列
  // STATIC_DRAW提示WebGL我们将怎么使用这些数据便于优化，这里提示不会经常改变这些数据。
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);

  // code above this line is initialization code.
  // code below this line is rendering code.

  /* 
   * function resizeCanvasToDisplaySize(canvas, multiplier) {
   *   multiplier = multiplier || 1;
   *   const width  = canvas.clientWidth  * multiplier | 0;
   *   const height = canvas.clientHeight * multiplier | 0;
   *   if (canvas.width !== width ||  canvas.height !== height) {
   *     canvas.width  = width;
   *     canvas.height = height;
   *     return true;
   *   }
   *   return false;
   * }
   */
  // gl.canvas的宽高创建时是默认值，所以需要手动复制为和canvas元素的宽高一致
  webglUtils.resizeCanvasToDisplaySize(gl.canvas);

  // Tell WebGL how to convert from clip space to pixels
  // webgl的裁剪空间坐标宽高都是（-1, 1），这里相当于把这个坐标映射到canvas元素上（0, gl.canvas.width）和（0, gl.canvas.height）
  gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

  // Clear the canvas
  // 设置清空画布使用clearColor指定的颜色填充
  gl.clearColor(0, 0, 0, 0);
  // 清空颜色缓冲区
  gl.clear(gl.COLOR_BUFFER_BIT);

  // Tell it to use our program (pair of shaders)
  gl.useProgram(program);

  // Turn on the attribute
  // 这里相当于告诉webgl我们将gl.vertexAttribPointer所指向的缓冲区来填充positionAttributeLocation这个位置
  // 一个隐藏信息是gl.vertexAttribPointer是将属性绑定到当前的ARRAY_BUFFER。 换句话说就是positionBuffer来填充a_position。
  gl.enableVertexAttribArray(positionAttributeLocation);

  // Bind the position buffer.
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

  // Tell the attribute how to get data out of positionBuffer (ARRAY_BUFFER)
  var size = 2;          // 2 components per iteration
  var type = gl.FLOAT;   // the data is 32bit floats
  var normalize = false; // don't normalize the data
  var stride = 0;        // 0 = move forward size * sizeof(type) each iteration to get the next position
  var offset = 0;        // start at the beginning of the buffer
  // 定义a_position如何从缓冲区中取数据
  // 这里size=2,attribute vec4 a_position是一个四元组向量，那么就只会填充前两个值
  gl.vertexAttribPointer(positionAttributeLocation, size, type, normalize, stride, offset);

  // draw
  var primitiveType = gl.TRIANGLES;
  var offset = 0;
  var count = 3;
  // 因为我们设置primitiveType（图元类型）为 gl.TRIANGLES（三角形）， 顶点着色器每运行三次WebGL将会根据三个gl_Position值绘制一个三角形
  // 这里运行三次，每次取一个点，也就是绘制一个三角形
  gl.drawArrays(primitiveType, offset, count);
}

main();
