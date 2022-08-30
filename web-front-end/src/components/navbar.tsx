import { Fragment } from "react";
import { Popover, Transition } from "@headlessui/react";
import {
  ArrowPathIcon,
  Bars3Icon,
  BookmarkSquareIcon,
  CalendarIcon,
  ChartBarIcon,
  CursorArrowRaysIcon,
  LifebuoyIcon,
  PhoneIcon,
  PlayIcon,
  ShieldCheckIcon,
  Squares2X2Icon,
  XMarkIcon,
} from "@heroicons/react/24/outline/index.js";
import { ChevronDownIcon } from "@heroicons/react/20/solid/index.js";

const solutions = [
  {
    name: "Contribue Research",
    description: "Have something to share? Reach out and let's chat",
    href: "/contribute-research",
    icon: ChartBarIcon,
  },
  {
    name: "Contribute Code",
    description: "Have code you want added to the site?",
    href: "#",
    icon: CursorArrowRaysIcon,
  },
];

const resources = [
  {
    name: "Research",
    description:
      "Get all of your questions answered in our forums or contact support.",
    href: "/research",
    icon: LifebuoyIcon,
  },
  {
    name: "Code",
    description:
      "Learn how to maximize our platform to get the most out of it.",
    href: "/research",
    icon: BookmarkSquareIcon,
  },
];

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

export default function Example() {
  return (
    <Popover className="relative bg-brandNeutral border-4 border-black">
      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <div className="flex items-center justify-between border-b-2 border-gray-100 py-6 md:justify-start md:space-x-10">
          <div className="flex justify-start lg:w-0 lg:flex-1">
            <a href="/">
              <span className="sr-only">Google Ads Open Research</span>
              <svg
                width="342"
                height="23"
                viewBox="0 0 342 23"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-auto"
              >
                <path
                  d="M5.296 18.24C4.24 18.24 3.32 18.04 2.536 17.64C1.768 17.24 1.168 16.664 0.736 15.912C0.32 15.144 0.112 14.24 0.112 13.2V5.28C0.112 4.224 0.32 3.32 0.736 2.568C1.168 1.816 1.768 1.24 2.536 0.839999C3.32 0.44 4.24 0.24 5.296 0.24C6.352 0.24 7.264 0.447999 8.032 0.863999C8.8 1.264 9.392 1.84 9.808 2.592C10.224 3.344 10.432 4.24 10.432 5.28H8.272C8.272 4.288 8.008 3.528 7.48 3C6.968 2.456 6.24 2.184 5.296 2.184C4.352 2.184 3.608 2.448 3.064 2.976C2.536 3.504 2.272 4.264 2.272 5.256V13.2C2.272 14.192 2.536 14.96 3.064 15.504C3.608 16.048 4.352 16.32 5.296 16.32C6.24 16.32 6.968 16.048 7.48 15.504C8.008 14.96 8.272 14.192 8.272 13.2V11.04H4.72V9.072H10.432V13.2C10.432 14.224 10.224 15.12 9.808 15.888C9.392 16.64 8.8 17.224 8.032 17.64C7.264 18.04 6.352 18.24 5.296 18.24ZM19.5906 18.192C18.5346 18.192 17.6226 17.992 16.8546 17.592C16.0866 17.192 15.4866 16.616 15.0546 15.864C14.6386 15.096 14.4306 14.192 14.4306 13.152V9.648C14.4306 8.592 14.6386 7.688 15.0546 6.936C15.4866 6.184 16.0866 5.608 16.8546 5.208C17.6226 4.808 18.5346 4.608 19.5906 4.608C20.6466 4.608 21.5586 4.808 22.3266 5.208C23.0946 5.608 23.6866 6.184 24.1026 6.936C24.5346 7.688 24.7506 8.584 24.7506 9.624V13.152C24.7506 14.192 24.5346 15.096 24.1026 15.864C23.6866 16.616 23.0946 17.192 22.3266 17.592C21.5586 17.992 20.6466 18.192 19.5906 18.192ZM19.5906 16.272C20.5346 16.272 21.2706 16.008 21.7986 15.48C22.3266 14.952 22.5906 14.176 22.5906 13.152V9.648C22.5906 8.624 22.3266 7.848 21.7986 7.32C21.2706 6.792 20.5346 6.528 19.5906 6.528C18.6626 6.528 17.9266 6.792 17.3826 7.32C16.8546 7.848 16.5906 8.624 16.5906 9.648V13.152C16.5906 14.176 16.8546 14.952 17.3826 15.48C17.9266 16.008 18.6626 16.272 19.5906 16.272ZM33.9813 18.192C32.9253 18.192 32.0133 17.992 31.2453 17.592C30.4773 17.192 29.8773 16.616 29.4453 15.864C29.0293 15.096 28.8213 14.192 28.8213 13.152V9.648C28.8213 8.592 29.0293 7.688 29.4453 6.936C29.8773 6.184 30.4773 5.608 31.2453 5.208C32.0133 4.808 32.9253 4.608 33.9813 4.608C35.0373 4.608 35.9493 4.808 36.7173 5.208C37.4853 5.608 38.0773 6.184 38.4933 6.936C38.9253 7.688 39.1413 8.584 39.1413 9.624V13.152C39.1413 14.192 38.9253 15.096 38.4933 15.864C38.0773 16.616 37.4853 17.192 36.7173 17.592C35.9493 17.992 35.0373 18.192 33.9813 18.192ZM33.9813 16.272C34.9253 16.272 35.6613 16.008 36.1893 15.48C36.7173 14.952 36.9813 14.176 36.9813 13.152V9.648C36.9813 8.624 36.7173 7.848 36.1893 7.32C35.6613 6.792 34.9253 6.528 33.9813 6.528C33.0533 6.528 32.3173 6.792 31.7733 7.32C31.2453 7.848 30.9813 8.624 30.9813 9.648V13.152C30.9813 14.176 31.2453 14.952 31.7733 15.48C32.3173 16.008 33.0533 16.272 33.9813 16.272ZM45.0359 22.32V20.352H49.2359C49.9079 20.352 50.3959 20.2 50.6999 19.896C51.0199 19.592 51.1799 19.12 51.1799 18.48V16.8L51.2279 14.4H50.7959L51.2039 14.04C51.2039 15 50.8839 15.76 50.2439 16.32C49.6039 16.88 48.7479 17.16 47.6759 17.16C46.3159 17.16 45.2439 16.72 44.4599 15.84C43.6759 14.944 43.2839 13.744 43.2839 12.24V9.456C43.2839 7.952 43.6759 6.76 44.4599 5.88C45.2439 5 46.3159 4.56 47.6759 4.56C48.7479 4.56 49.6039 4.84 50.2439 5.4C50.8839 5.96 51.2039 6.72 51.2039 7.68L50.7959 7.32H51.2039V4.8H53.3399V18.48C53.3399 19.664 52.9719 20.6 52.2359 21.288C51.5159 21.976 50.5079 22.32 49.2119 22.32H45.0359ZM48.3239 15.288C49.2199 15.288 49.9239 15.008 50.4359 14.448C50.9479 13.888 51.2039 13.112 51.2039 12.12V9.6C51.2039 8.608 50.9479 7.832 50.4359 7.272C49.9239 6.712 49.2199 6.432 48.3239 6.432C47.4119 6.432 46.6999 6.704 46.1879 7.248C45.6919 7.792 45.4439 8.576 45.4439 9.6V12.12C45.4439 13.144 45.6919 13.928 46.1879 14.472C46.6999 15.016 47.4119 15.288 48.3239 15.288ZM64.5625 18C63.7945 18 63.1225 17.848 62.5465 17.544C61.9705 17.24 61.5225 16.808 61.2025 16.248C60.8825 15.688 60.7225 15.032 60.7225 14.28V2.448H56.2825V0.48H62.8825V14.28C62.8825 14.824 63.0345 15.256 63.3385 15.576C63.6425 15.88 64.0505 16.032 64.5625 16.032H68.7625V18H64.5625ZM77.1531 18.24C76.1131 18.24 75.2011 18.032 74.4171 17.616C73.6491 17.2 73.0491 16.616 72.6171 15.864C72.2011 15.096 71.9931 14.208 71.9931 13.2V9.6C71.9931 8.576 72.2011 7.688 72.6171 6.936C73.0491 6.184 73.6491 5.6 74.4171 5.184C75.2011 4.768 76.1131 4.56 77.1531 4.56C78.1931 4.56 79.0971 4.768 79.8651 5.184C80.6491 5.6 81.2491 6.184 81.6651 6.936C82.0971 7.688 82.3131 8.576 82.3131 9.6V11.928H74.1051V13.2C74.1051 14.24 74.3691 15.04 74.8971 15.6C75.4251 16.144 76.1771 16.416 77.1531 16.416C77.9851 16.416 78.6571 16.272 79.1691 15.984C79.6811 15.68 79.9931 15.232 80.1051 14.64H82.2651C82.1211 15.744 81.5771 16.624 80.6331 17.28C79.7051 17.92 78.5451 18.24 77.1531 18.24ZM80.2011 10.488V9.6C80.2011 8.56 79.9371 7.76 79.4091 7.2C78.8971 6.64 78.1451 6.36 77.1531 6.36C76.1771 6.36 75.4251 6.64 74.8971 7.2C74.3691 7.76 74.1051 8.56 74.1051 9.6V10.296H80.3691L80.2011 10.488ZM99.9344 18L104.494 0.48H107.398L111.934 18H109.75L108.598 13.344H103.294L102.142 18H99.9344ZM103.726 11.52H108.142L106.798 6.12C106.542 5.096 106.342 4.24 106.198 3.552C106.054 2.864 105.966 2.416 105.934 2.208C105.902 2.416 105.814 2.864 105.67 3.552C105.526 4.24 105.326 5.088 105.07 6.096L103.726 11.52ZM119.557 18.24C118.245 18.24 117.181 17.8 116.365 16.92C115.565 16.04 115.165 14.848 115.165 13.344V9.48C115.165 7.96 115.565 6.76 116.365 5.88C117.165 5 118.229 4.56 119.557 4.56C120.645 4.56 121.517 4.856 122.173 5.448C122.829 6.04 123.157 6.832 123.157 7.824L122.725 7.32H123.205L123.157 4.32V0.48H125.317V18H123.157V15.48H122.725L123.157 14.976C123.157 15.984 122.829 16.784 122.173 17.376C121.517 17.952 120.645 18.24 119.557 18.24ZM120.277 16.368C121.173 16.368 121.877 16.088 122.389 15.528C122.901 14.968 123.157 14.192 123.157 13.2V9.6C123.157 8.608 122.901 7.832 122.389 7.272C121.877 6.712 121.173 6.432 120.277 6.432C119.365 6.432 118.645 6.704 118.117 7.248C117.589 7.792 117.325 8.576 117.325 9.6V13.2C117.325 14.224 117.589 15.008 118.117 15.552C118.645 16.096 119.365 16.368 120.277 16.368ZM134.308 18.192C133.412 18.192 132.628 18.056 131.956 17.784C131.3 17.496 130.772 17.096 130.372 16.584C129.988 16.072 129.756 15.464 129.676 14.76H131.836C131.932 15.224 132.188 15.592 132.604 15.864C133.036 16.136 133.604 16.272 134.308 16.272H135.316C136.164 16.272 136.796 16.104 137.212 15.768C137.628 15.416 137.836 14.952 137.836 14.376C137.836 13.816 137.644 13.376 137.26 13.056C136.892 12.72 136.34 12.496 135.604 12.384L133.828 12.096C132.532 11.872 131.564 11.472 130.924 10.896C130.3 10.304 129.988 9.448 129.988 8.328C129.988 7.144 130.364 6.232 131.116 5.592C131.868 4.936 132.996 4.608 134.5 4.608H135.412C136.676 4.608 137.692 4.904 138.46 5.496C139.228 6.088 139.692 6.888 139.852 7.896H137.692C137.596 7.48 137.356 7.152 136.972 6.912C136.588 6.656 136.068 6.528 135.412 6.528H134.5C133.684 6.528 133.084 6.68 132.7 6.984C132.332 7.288 132.148 7.744 132.148 8.352C132.148 8.896 132.308 9.296 132.628 9.552C132.948 9.808 133.452 9.992 134.14 10.104L135.916 10.392C137.34 10.616 138.372 11.032 139.012 11.64C139.668 12.248 139.996 13.128 139.996 14.28C139.996 15.496 139.604 16.456 138.82 17.16C138.052 17.848 136.884 18.192 135.316 18.192H134.308ZM163.497 18.24C162.441 18.24 161.529 18.04 160.761 17.64C160.009 17.24 159.425 16.664 159.009 15.912C158.609 15.144 158.409 14.24 158.409 13.2V5.28C158.409 4.224 158.609 3.32 159.009 2.568C159.425 1.816 160.009 1.24 160.761 0.839999C161.529 0.44 162.441 0.24 163.497 0.24C164.553 0.24 165.457 0.44 166.209 0.839999C166.977 1.24 167.561 1.816 167.961 2.568C168.377 3.32 168.585 4.216 168.585 5.256V13.2C168.585 14.24 168.377 15.144 167.961 15.912C167.561 16.664 166.977 17.24 166.209 17.64C165.457 18.04 164.553 18.24 163.497 18.24ZM163.497 16.296C164.441 16.296 165.161 16.032 165.657 15.504C166.169 14.96 166.425 14.192 166.425 13.2V5.28C166.425 4.288 166.169 3.528 165.657 3C165.161 2.456 164.441 2.184 163.497 2.184C162.569 2.184 161.849 2.456 161.337 3C160.825 3.528 160.569 4.288 160.569 5.28V13.2C160.569 14.192 160.825 14.96 161.337 15.504C161.849 16.032 162.569 16.296 163.497 16.296ZM172.896 22.32V4.8H175.056V7.32H175.488L175.056 7.824C175.056 6.816 175.384 6.024 176.04 5.448C176.712 4.856 177.592 4.56 178.68 4.56C180.008 4.56 181.064 5 181.848 5.88C182.648 6.744 183.048 7.936 183.048 9.456V13.32C183.048 14.328 182.864 15.2 182.496 15.936C182.144 16.672 181.64 17.24 180.984 17.64C180.344 18.04 179.576 18.24 178.68 18.24C177.608 18.24 176.736 17.944 176.064 17.352C175.392 16.76 175.056 15.968 175.056 14.976L175.488 15.48H175.008L175.056 18.48V22.32H172.896ZM177.96 16.368C178.872 16.368 179.584 16.096 180.096 15.552C180.624 15.008 180.888 14.224 180.888 13.2V9.6C180.888 8.576 180.624 7.792 180.096 7.248C179.584 6.704 178.872 6.432 177.96 6.432C177.08 6.432 176.376 6.712 175.848 7.272C175.32 7.832 175.056 8.608 175.056 9.6V13.2C175.056 14.192 175.32 14.968 175.848 15.528C176.376 16.088 177.08 16.368 177.96 16.368ZM192.278 18.24C191.238 18.24 190.326 18.032 189.542 17.616C188.774 17.2 188.174 16.616 187.742 15.864C187.326 15.096 187.118 14.208 187.118 13.2V9.6C187.118 8.576 187.326 7.688 187.742 6.936C188.174 6.184 188.774 5.6 189.542 5.184C190.326 4.768 191.238 4.56 192.278 4.56C193.318 4.56 194.222 4.768 194.99 5.184C195.774 5.6 196.374 6.184 196.79 6.936C197.222 7.688 197.438 8.576 197.438 9.6V11.928H189.23V13.2C189.23 14.24 189.494 15.04 190.022 15.6C190.55 16.144 191.302 16.416 192.278 16.416C193.11 16.416 193.782 16.272 194.294 15.984C194.806 15.68 195.118 15.232 195.23 14.64H197.39C197.246 15.744 196.702 16.624 195.758 17.28C194.83 17.92 193.67 18.24 192.278 18.24ZM195.326 10.488V9.6C195.326 8.56 195.062 7.76 194.534 7.2C194.022 6.64 193.27 6.36 192.278 6.36C191.302 6.36 190.55 6.64 190.022 7.2C189.494 7.76 189.23 8.56 189.23 9.6V10.296H195.494L195.326 10.488ZM201.677 18V4.8H203.837V7.32H204.293L203.837 7.824C203.837 6.784 204.149 5.984 204.773 5.424C205.397 4.848 206.261 4.56 207.365 4.56C208.693 4.56 209.749 4.968 210.533 5.784C211.317 6.6 211.709 7.712 211.709 9.12V18H209.549V9.36C209.549 8.416 209.293 7.696 208.781 7.2C208.285 6.688 207.605 6.432 206.741 6.432C205.845 6.432 205.133 6.704 204.605 7.248C204.093 7.792 203.837 8.576 203.837 9.6V18H201.677ZM230.458 18V0.48H235.882C236.922 0.48 237.834 0.696 238.618 1.128C239.402 1.544 240.01 2.128 240.442 2.88C240.874 3.632 241.09 4.512 241.09 5.52C241.09 6.704 240.778 7.72 240.154 8.568C239.546 9.416 238.714 10 237.658 10.32L241.33 18H238.786L235.426 10.56H232.618V18H230.458ZM232.618 8.616H235.882C236.778 8.616 237.498 8.336 238.042 7.776C238.586 7.2 238.858 6.448 238.858 5.52C238.858 4.576 238.586 3.824 238.042 3.264C237.498 2.704 236.778 2.424 235.882 2.424H232.618V8.616ZM249.841 18.24C248.801 18.24 247.889 18.032 247.105 17.616C246.337 17.2 245.737 16.616 245.305 15.864C244.889 15.096 244.681 14.208 244.681 13.2V9.6C244.681 8.576 244.889 7.688 245.305 6.936C245.737 6.184 246.337 5.6 247.105 5.184C247.889 4.768 248.801 4.56 249.841 4.56C250.881 4.56 251.785 4.768 252.553 5.184C253.337 5.6 253.937 6.184 254.353 6.936C254.785 7.688 255.001 8.576 255.001 9.6V11.928H246.793V13.2C246.793 14.24 247.057 15.04 247.585 15.6C248.113 16.144 248.865 16.416 249.841 16.416C250.673 16.416 251.345 16.272 251.857 15.984C252.369 15.68 252.681 15.232 252.793 14.64H254.953C254.809 15.744 254.265 16.624 253.321 17.28C252.393 17.92 251.233 18.24 249.841 18.24ZM252.889 10.488V9.6C252.889 8.56 252.625 7.76 252.097 7.2C251.585 6.64 250.833 6.36 249.841 6.36C248.865 6.36 248.113 6.64 247.585 7.2C247.057 7.76 246.793 8.56 246.793 9.6V10.296H253.057L252.889 10.488ZM263.823 18.192C262.927 18.192 262.143 18.056 261.471 17.784C260.815 17.496 260.287 17.096 259.887 16.584C259.503 16.072 259.271 15.464 259.191 14.76H261.351C261.447 15.224 261.703 15.592 262.119 15.864C262.551 16.136 263.119 16.272 263.823 16.272H264.831C265.679 16.272 266.311 16.104 266.727 15.768C267.143 15.416 267.351 14.952 267.351 14.376C267.351 13.816 267.159 13.376 266.775 13.056C266.407 12.72 265.855 12.496 265.119 12.384L263.343 12.096C262.047 11.872 261.079 11.472 260.439 10.896C259.815 10.304 259.503 9.448 259.503 8.328C259.503 7.144 259.879 6.232 260.631 5.592C261.383 4.936 262.511 4.608 264.015 4.608H264.927C266.191 4.608 267.207 4.904 267.975 5.496C268.743 6.088 269.207 6.888 269.367 7.896H267.207C267.111 7.48 266.871 7.152 266.487 6.912C266.103 6.656 265.583 6.528 264.927 6.528H264.015C263.199 6.528 262.599 6.68 262.215 6.984C261.847 7.288 261.663 7.744 261.663 8.352C261.663 8.896 261.823 9.296 262.143 9.552C262.463 9.808 262.967 9.992 263.655 10.104L265.431 10.392C266.855 10.616 267.887 11.032 268.527 11.64C269.183 12.248 269.511 13.128 269.511 14.28C269.511 15.496 269.119 16.456 268.335 17.16C267.567 17.848 266.399 18.192 264.831 18.192H263.823ZM278.622 18.24C277.582 18.24 276.67 18.032 275.886 17.616C275.118 17.2 274.518 16.616 274.086 15.864C273.67 15.096 273.462 14.208 273.462 13.2V9.6C273.462 8.576 273.67 7.688 274.086 6.936C274.518 6.184 275.118 5.6 275.886 5.184C276.67 4.768 277.582 4.56 278.622 4.56C279.662 4.56 280.566 4.768 281.334 5.184C282.118 5.6 282.718 6.184 283.134 6.936C283.566 7.688 283.782 8.576 283.782 9.6V11.928H275.574V13.2C275.574 14.24 275.838 15.04 276.366 15.6C276.894 16.144 277.646 16.416 278.622 16.416C279.454 16.416 280.126 16.272 280.638 15.984C281.15 15.68 281.462 15.232 281.574 14.64H283.734C283.59 15.744 283.046 16.624 282.102 17.28C281.174 17.92 280.014 18.24 278.622 18.24ZM281.67 10.488V9.6C281.67 8.56 281.406 7.76 280.878 7.2C280.366 6.64 279.614 6.36 278.622 6.36C277.646 6.36 276.894 6.64 276.366 7.2C275.838 7.76 275.574 8.56 275.574 9.6V10.296H281.838L281.67 10.488ZM291.861 18.24C290.469 18.24 289.373 17.888 288.573 17.184C287.773 16.464 287.373 15.496 287.373 14.28C287.373 13.048 287.773 12.08 288.573 11.376C289.373 10.672 290.453 10.32 291.812 10.32H295.893V9C295.893 8.184 295.645 7.56 295.149 7.128C294.669 6.68 293.981 6.456 293.085 6.456C292.301 6.456 291.645 6.624 291.117 6.96C290.589 7.28 290.285 7.72 290.205 8.28H288.045C288.189 7.144 288.725 6.24 289.653 5.568C290.581 4.896 291.741 4.56 293.133 4.56C294.653 4.56 295.853 4.952 296.733 5.736C297.613 6.52 298.053 7.584 298.053 8.928V18H295.941V15.48H295.581L295.941 15.12C295.941 16.08 295.565 16.84 294.813 17.4C294.077 17.96 293.093 18.24 291.861 18.24ZM292.389 16.536C293.413 16.536 294.253 16.28 294.909 15.768C295.565 15.256 295.893 14.6 295.893 13.8V11.928H291.861C291.141 11.928 290.573 12.128 290.157 12.528C289.741 12.928 289.533 13.472 289.533 14.16C289.533 14.896 289.781 15.48 290.277 15.912C290.789 16.328 291.493 16.536 292.389 16.536ZM302.867 18V4.8H304.979V7.32H305.483L304.787 8.88C304.787 7.456 305.091 6.384 305.699 5.664C306.323 4.928 307.243 4.56 308.459 4.56C309.851 4.56 310.955 5 311.771 5.88C312.603 6.744 313.019 7.92 313.019 9.408V10.2H310.859V9.6C310.859 8.56 310.603 7.768 310.091 7.224C309.595 6.664 308.883 6.384 307.955 6.384C307.043 6.384 306.323 6.664 305.795 7.224C305.283 7.784 305.027 8.576 305.027 9.6V18H302.867ZM321.89 18.24C320.834 18.24 319.906 18.04 319.106 17.64C318.322 17.24 317.714 16.664 317.282 15.912C316.85 15.144 316.634 14.24 316.634 13.2V9.6C316.634 8.544 316.85 7.64 317.282 6.888C317.714 6.136 318.322 5.56 319.106 5.16C319.906 4.76 320.834 4.56 321.89 4.56C323.41 4.56 324.634 4.968 325.562 5.784C326.49 6.6 326.978 7.712 327.026 9.12H324.866C324.818 8.272 324.53 7.624 324.002 7.176C323.49 6.712 322.786 6.48 321.89 6.48C320.946 6.48 320.194 6.752 319.634 7.296C319.074 7.824 318.794 8.584 318.794 9.576V13.2C318.794 14.192 319.074 14.96 319.634 15.504C320.194 16.048 320.946 16.32 321.89 16.32C322.786 16.32 323.49 16.088 324.002 15.624C324.53 15.16 324.818 14.512 324.866 13.68H327.026C326.978 15.088 326.49 16.2 325.562 17.016C324.634 17.832 323.41 18.24 321.89 18.24ZM331.192 18V0.48H333.352V4.8V7.32H333.808L333.352 7.824C333.352 6.784 333.664 5.984 334.288 5.424C334.912 4.848 335.776 4.56 336.88 4.56C338.208 4.56 339.264 4.968 340.048 5.784C340.832 6.6 341.224 7.712 341.224 9.12V18H339.064V9.36C339.064 8.416 338.808 7.688 338.296 7.176C337.8 6.648 337.12 6.384 336.256 6.384C335.36 6.384 334.648 6.664 334.12 7.224C333.608 7.784 333.352 8.576 333.352 9.6V18H331.192Z"
                  fill="black"
                />
              </svg>
            </a>
          </div>
          <div className="-my-2 -mr-2 md:hidden">
            <Popover.Button className="inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-brand-cta">
              <span className="sr-only">Open menu</span>
              <Bars3Icon className="h-6 w-6" aria-hidden="true" />
            </Popover.Button>
          </div>
          {/* @ts-ignore */}
          <Popover.Group as="nav" className="hidden space-x-10 md:flex">
            <Popover className="relative">
              {({ open }: { open: boolean }) => (
                <>
                  <Popover.Button
                    className={classNames(
                      open ? "text-gray-900" : "text-gray-500",
                      "group inline-flex items-center rounded-md bg-brandNeutral text-base font-medium hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-brand-cta focus:ring-offset-2"
                    )}
                  >
                    <span>Contributing</span>
                    <ChevronDownIcon
                      className={classNames(
                        open ? "text-gray-600" : "text-gray-400",
                        "ml-2 h-5 w-5 group-hover:text-gray-500"
                      )}
                      aria-hidden="true"
                    />
                  </Popover.Button>
                  <Transition
                    as={Fragment}
                    enter="transition ease-out duration-200"
                    enterFrom="opacity-0 translate-y-1"
                    enterTo="opacity-100 translate-y-0"
                    leave="transition ease-in duration-150"
                    leaveFrom="opacity-100 translate-y-0"
                    leaveTo="opacity-0 translate-y-1"
                  >
                    <Popover.Panel className="absolute z-10 -ml-4 mt-3 w-screen max-w-md transform px-2 sm:px-0 lg:left-1/2 lg:ml-0 lg:-translate-x-1/2">
                      <div className="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5">
                        <div className="relative grid gap-6 bg-white px-5 py-6 sm:gap-8 sm:p-8">
                          {solutions.map((item) => (
                            <a
                              key={item.name}
                              href={item.href}
                              className="-m-3 flex items-start rounded-lg p-3 hover:bg-gray-50"
                            >
                              <item.icon
                                className="h-6 w-6 flex-shrink-0 text-brandCTA-dark"
                                aria-hidden="true"
                              />
                              <div className="ml-4">
                                <p className="text-base font-medium text-gray-900">
                                  {item.name}
                                </p>
                                <p className="mt-1 text-sm text-gray-500">
                                  {item.description}
                                </p>
                              </div>
                            </a>
                          ))}
                        </div>
                      </div>
                    </Popover.Panel>
                  </Transition>
                </>
              )}
            </Popover>
            <a
              href="/research"
              className="text-base font-medium text-gray-500 hover:text-gray-900"
            >
              Research
            </a>

            <a
              href="/about"
              className="text-base font-medium text-gray-500 hover:text-gray-900"
            >
              About
            </a>
            <a
              href="/contact"
              className="text-base font-medium text-gray-500 hover:text-gray-900"
            >
              Contact
            </a>
          </Popover.Group>
        </div>
      </div>

      <Transition
        as={Fragment}
        enter="duration-200 ease-out"
        enterFrom="opacity-0 scale-95"
        enterTo="opacity-100 scale-100"
        leave="duration-100 ease-in"
        leaveFrom="opacity-100 scale-100"
        leaveTo="opacity-0 scale-95"
      >
        <Popover.Panel
          focus
          className="absolute inset-x-0 top-0 origin-top-right transform p-2 transition md:hidden"
        >
          <div className="divide-y-2 divide-gray-50 rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5">
            <div className="px-5 pt-5 pb-6">
              <div className="flex items-center justify-between">
                <div>
                  <img
                    className="h-8 w-auto"
                    src="https://tailwindui.com/img/logos/workflow-mark.svg?color=indigo&shade=600"
                    alt="Workflow"
                  />
                </div>
                <div className="-mr-2">
                  <Popover.Button className="inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-brand-cta">
                    <span className="sr-only">Close menu</span>
                    <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                  </Popover.Button>
                </div>
              </div>
              <div className="mt-6">
                <nav className="grid gap-y-8">
                  {solutions.map((item) => (
                    <a
                      key={item.name}
                      href={item.href}
                      className="-m-3 flex items-center rounded-md p-3 hover:bg-gray-50"
                    >
                      <item.icon
                        className="h-6 w-6 flex-shrink-0 text-brandCTA-dark"
                        aria-hidden="true"
                      />
                      <span className="ml-3 text-base font-medium text-gray-900">
                        {item.name}
                      </span>
                    </a>
                  ))}
                </nav>
              </div>
            </div>
            <div className="space-y-6 py-6 px-5">
              <div className="grid grid-cols-2 gap-y-4 gap-x-8">
                <a
                  href="/about"
                  className="text-base font-medium text-gray-900 hover:text-gray-700"
                >
                  About
                </a>

                <a
                  href="#"
                  className="text-base font-medium text-gray-900 hover:text-gray-700"
                >
                  Contact
                </a>
                {resources.map((item) => (
                  <a
                    key={item.name}
                    href={item.href}
                    className="text-base font-medium text-gray-900 hover:text-gray-700"
                  >
                    {item.name}
                  </a>
                ))}
              </div>
            </div>
          </div>
        </Popover.Panel>
      </Transition>
    </Popover>
  );
}
