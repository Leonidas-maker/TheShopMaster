import * as React from "react"
import Svg, { Path, Circle } from "react-native-svg"

function InfoSVG(props: any) {
  return (
    <Svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      width={512}
      height={512}
      {...props}
    >
      <Path d="M12 0a12 12 0 1012 12A12.013 12.013 0 0012 0zm0 22a10 10 0 1110-10 10.011 10.011 0 01-10 10z" />
      <Path d="M12 10h-1a1 1 0 000 2h1v6a1 1 0 002 0v-6a2 2 0 00-2-2z" />
      <Circle cx={12} cy={6.5} r={1.5} />
    </Svg>
  )
}

export default InfoSVG;