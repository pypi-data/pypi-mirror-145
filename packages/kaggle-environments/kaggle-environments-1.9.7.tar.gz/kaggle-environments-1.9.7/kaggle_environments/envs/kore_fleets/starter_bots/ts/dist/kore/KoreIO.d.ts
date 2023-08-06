import { Board } from "./Board";
export declare class KoreIO {
    getLine: () => Promise<string>;
    _setup(): void;
    /**
     * Constructor for a new agent
     * User should edit this according to the `Design` this agent will compete under
     */
    constructor();
    run(loop: (board: Board) => Board): Promise<void>;
}
