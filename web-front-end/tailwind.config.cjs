/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
	theme: {
		extend: {
			colors: {
				brandNeutral: {
					DEFAULT: "#FDF8EC",
					dark: "#FBECD8"
				},
				brandCTA:{
					DEFAULT: "#FFE040",
					dark: "#D7B400"
				}
			}
		},
	},
	plugins: [],
}
