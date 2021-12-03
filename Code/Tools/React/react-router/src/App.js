import * as React from "react";
import { Routes, Route, Link, matchPath, useLocation } from "react-router-dom";

function Home() {
  return (
    <>
      <main>
        <h2>Welcome to the homepage!</h2>
        <p>You can do this, I believe in you.</p>
      </main>
      <nav>
        <Link to="/test/about">About</Link>
      </nav>
    </>
  );
}

function About() {
  let location = useLocation();
  // 获取当前url
  const pathname = location.pathname;
  console.log(pathname);
  // 解析当前路径
  const PathMath = matchPath("test/:id", pathname);
  console.log(PathMath.pathname, PathMath.params)
  return (
    <>
      <main>
        <h2>Who are we?</h2>
        <p>
          That feels like an existential question, don't you
          think?
        </p>
      </main>
      <nav>
        <Link to="/">Home</Link>
      </nav>
    </>
  );
}

// 创建了两个页面 / 和　/about
// 被嵌套进了html中，使得其他的外围的Welcome to React Router!可以在两个页面中都保留
function App() {
  return (
    <div className="App">
      <h1>Welcome to React Router!</h1>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/test/about" element={<About />} />
      </Routes>
    </div>
  );
}

export default App;
