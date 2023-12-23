import * as React from "react"
import Svg, { Path } from "react-native-svg"

function UserSVG(props: any) {
  return (
    <Svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      width={512}
      height={512}
      {...props}
    >
      <Path d="M12 12a6 6 0 10-6-6 6.006 6.006 0 006 6zm0-10a4 4 0 11-4 4 4 4 0 014-4zM12 14a9.01 9.01 0 00-9 9 1 1 0 002 0 7 7 0 0114 0 1 1 0 002 0 9.01 9.01 0 00-9-9z" />
    </Svg>
  )
}

export default UserSVG