'use client';

import { useRef } from "react";
import gasp from "gsap";
import { useGSAP } from "@gsap/react";

gasp.registerPlugin(useGSAP);

export default function Home() {
  const container = useRef();
  const { contextSafe } = useGSAP({ scope: container});

  useGSAP(() => {
      gasp.to('.box', { x: 360 });
    },
    {scope: container}
  );

  const onClickGood = contextSafe(() => {
    gasp.to('.good', { rotation: "+=360" })
  })

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <div ref={container} className="container">
        <div className="box w-28 h-28 bg-red-500">test</div>
        <button onClick={onClickGood} className="good w-28 h-28 bg-blue-50">hah</button>
      </div>
    </div>
  );
}
