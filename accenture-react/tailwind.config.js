module.exports = {
content: ["./index.html", "./src/**/*.{js,jsx}"],
theme: {
extend: {
colors: {
accenture: "#A100FF",
accentureDark: "#33004D",
},
animation: {
fadeIn: "fadeIn 1s ease-in-out",
},
keyframes: {
fadeIn: {
"0%": { opacity: 0 },
"100%": { opacity: 1 },
},
},
},
},
plugins: [],
};