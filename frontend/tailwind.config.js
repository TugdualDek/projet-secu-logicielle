/** @type {import('tailwindcss').Config} */

module.exports = {
	darkMode: ["class"],
    content: [
		"./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
		"./src/components/**/*.{js,ts,jsx,tsx,mdx}",
		"./src/app/**/*.{js,ts,jsx,tsx,mdx}",
	],
	theme: {
		extend: {
			colors: {
				"red": "#D0021B",
				"green": "#03D27F",
				background: {
					"primary": "#0B1117",
					"secondary": "#EEEFF3",
					"tertiary": "#3A3B41",
				},
				foreground :{
					"secondary": "#83848E",
				},
				border: {
					"primary": "#F3F5F9"
				}
			}
		}
	},
  	plugins: [require("tailwindcss-animate")],
};
