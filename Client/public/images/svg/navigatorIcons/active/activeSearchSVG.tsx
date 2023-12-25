import * as React from "react"
import Svg, { Path } from "react-native-svg"

function ActiveSearchSVG(props: any) {
  return (
    <Svg
      xmlns="http://www.w3.org/2000/svg"
      x="0px"
      y="0px"
      viewBox="0 0 511.786 511.786"
      xmlSpace="preserve"
      width={512}
      height={512}
      enableBackground="new 0 0 511.786 511.786"
      {...props}
    >
      <Path d="M213.382 426.694a212.415 212.415 0 00134.976-48.171l127.275 127.253c8.475 8.185 21.98 7.95 30.165-.525 7.984-8.267 7.984-21.373 0-29.641L378.545 348.337c74.545-91.24 61.011-225.636-30.229-300.181S122.68-12.855 48.135 78.385-12.876 304.02 78.364 378.566a213.331 213.331 0 00135.018 48.128z" />
    </Svg>
  )
}

export default ActiveSearchSVG