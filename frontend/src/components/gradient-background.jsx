const GradientBackground = () => {
    return (
        <div className="absolute z-10 inset-0 h-[100vh] backdrop-blur-[100px] bg-[#ffffff03]">
            <div className="h-full bg-[radial-gradient(ellipse_100%_100%_at_bottom,rgba(0,0,0,0)_50%,rgba(106,20,255,0.5)_75%,#6A14FF_90%,#BA93FF_100%)]" />
        </div>
    );
}
 
export default GradientBackground;