import * as React from "react"
import Svg, { Path } from "react-native-svg"

function ScannerSVG(props: any) {
  return (
    <Svg
      xmlns="http://www.w3.org/2000/svg"
      data-name="Layer 1"
      viewBox="0 0 24 24"
      {...props}
    >
      <Path d="M24 12a1 1 0 01-1 1H1a1 1 0 010-2h22a1 1 0 011 1zM7 22H5c-1.654 0-3-1.346-3-3v-2a1 1 0 00-2 0v2c0 2.757 2.243 5 5 5h2a1 1 0 000-2zm16-6a1 1 0 00-1 1v2c0 1.654-1.346 3-3 3h-2a1 1 0 000 2h2c2.757 0 5-2.243 5-5v-2a1 1 0 00-1-1zM19 0h-2a1 1 0 000 2h2c1.654 0 3 1.346 3 3v2a1 1 0 002 0V5c0-2.757-2.243-5-5-5zM1 8a1 1 0 001-1V5c0-1.654 1.346-3 3-3h2a1 1 0 000-2H5C2.243 0 0 2.243 0 5v2a1 1 0 001 1z" />
    </Svg>
  )
}

export default ScannerSVG