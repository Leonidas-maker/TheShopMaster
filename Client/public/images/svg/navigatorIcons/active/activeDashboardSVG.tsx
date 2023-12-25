import * as React from "react"
import Svg, { Path } from "react-native-svg"

function ActiveDashboardSVG(props: any) {
  return (
    <Svg
      xmlns="http://www.w3.org/2000/svg"
      x="0px"
      y="0px"
      viewBox="0 0 512 512"
      xmlSpace="preserve"
      width={512}
      height={512}
      enableBackground="new 0 0 512 512"
      {...props}
    >
      <Path d="M256 319.841c-35.346 0-64 28.654-64 64v128h128v-128c0-35.346-28.654-64-64-64z" />
      <Path d="M362.667 383.841v128H448c35.346 0 64-28.654 64-64V253.26a42.665 42.665 0 00-12.011-29.696l-181.29-195.99c-31.988-34.61-85.976-36.735-120.586-4.747a85.355 85.355 0 00-4.747 4.747L12.395 223.5A42.669 42.669 0 000 253.58v194.261c0 35.346 28.654 64 64 64h85.333v-128c.399-58.172 47.366-105.676 104.073-107.044 58.604-1.414 108.814 46.899 109.261 107.044z" />
      <Path d="M256 319.841c-35.346 0-64 28.654-64 64v128h128v-128c0-35.346-28.654-64-64-64z" />
    </Svg>
  )
}

export default ActiveDashboardSVG