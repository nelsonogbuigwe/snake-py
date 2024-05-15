'use client';
import React, {useEffect, useRef, useState} from 'react';
import dynamic from 'next/dynamic';
// import styles from './SnakeGame.module.css'; // Add CSS styles if needed

const PygbagGame = dynamic(() => import('../public/wasm/game'), {ssr: false});

export default function SnakeGame() {
    const canvasRef = useRef(null);
    const [gameModule, setGameModule] = useState(null);

    useEffect(() => {
        async function loadGame() {
            const module = await PygbagGame();
            setGameModule(module);
            module.startGame(canvasRef.current);
        }

        loadGame();
    }, []);

    useEffect(() => {
        const handleResize = () => {
            if (gameModule && canvasRef.current) {
                gameModule.resizeGame(canvasRef.current);
            }
        };

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, [gameModule]);

    return (
        <div className={styles.gameContainer}>
            <canvas ref={canvasRef}/>
        </div>
    );
}
