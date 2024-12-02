const GradientBackground = () => {
    return (
        <div className="absolute -z-10 inset-0 h-[200vh] backdrop-blur-[100px] bg-[#ffffff03]">
            <div className="bg-radial-[at_25%_25%] from-white to-zinc-900 to-75%" />
        </div>
    );
}
 
export default GradientBackground;