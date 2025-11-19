import { useEffect, useRef } from "react";

export default function AudioOrb({ isSpeaking, volume = 0.5 }) {
  const canvasRef = useRef(null);
  const animationRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const baseRadius = 60;
    let phase = 0;

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Background glow
      const gradient = ctx.createRadialGradient(
        centerX,
        centerY,
        0,
        centerX,
        centerY,
        baseRadius * 2
      );
      gradient.addColorStop(0, "rgba(168, 85, 247, 0.4)");
      gradient.addColorStop(0.5, "rgba(168, 85, 247, 0.2)");
      gradient.addColorStop(1, "rgba(168, 85, 247, 0)");

      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Animated orb rings
      const rings = 5;
      for (let i = 0; i < rings; i++) {
        const offset = (phase + i * 0.5) % (Math.PI * 2);
        const scale = isSpeaking ? 1 + Math.sin(offset) * 0.3 * volume : 1;
        const radius = baseRadius * scale * (1 + i * 0.15);
        const alpha = isSpeaking
          ? 0.6 - i * 0.1 - Math.abs(Math.sin(offset)) * 0.2
          : 0.3 - i * 0.05;

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(168, 85, 247, ${alpha})`;
        ctx.lineWidth = 2;
        ctx.stroke();
      }

      // Core orb
      const coreGradient = ctx.createRadialGradient(
        centerX,
        centerY,
        0,
        centerX,
        centerY,
        baseRadius
      );
      coreGradient.addColorStop(0, "rgba(216, 180, 254, 1)");
      coreGradient.addColorStop(0.7, "rgba(168, 85, 247, 0.9)");
      coreGradient.addColorStop(1, "rgba(126, 34, 206, 0.8)");

      ctx.fillStyle = coreGradient;
      ctx.beginPath();
      ctx.arc(centerX, centerY, baseRadius, 0, Math.PI * 2);
      ctx.fill();

      // Pulse effect when speaking
      if (isSpeaking) {
        phase += 0.05;
      }

      animationRef.current = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [isSpeaking, volume]);

  return (
    <canvas ref={canvasRef} width={300} height={300} className="mx-auto" />
  );
}
