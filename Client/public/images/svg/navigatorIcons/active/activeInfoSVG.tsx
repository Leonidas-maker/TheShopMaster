import * as React from "react"
import Svg, { Path } from "react-native-svg"

function ActiveInfoSVG(props: any) {
  return (
    <Svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      width={512}
      height={512}
      {...props}
    >
      <Path d="M12 24A12 12 0 100 12a12.013 12.013 0 0012 12zm0-19a1.5 1.5 0 11-1.5 1.5A1.5 1.5 0 0112 5zm-1 5h1a2 2 0 012 2v6a1 1 0 01-2 0v-6h-1a1 1 0 010-2z" />
    </Svg>
  )
}

export default ActiveInfoSVG;