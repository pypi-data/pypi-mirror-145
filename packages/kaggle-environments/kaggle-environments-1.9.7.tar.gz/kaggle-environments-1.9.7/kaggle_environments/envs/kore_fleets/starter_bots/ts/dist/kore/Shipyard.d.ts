import { Board } from "./Board";
import { Cell } from "./Cell";
import { Player } from "./Player";
import { Point } from "./Point";
import { ShipyardAction } from "./ShipyardAction";
export declare class Shipyard {
    readonly id: string;
    shipCount: number;
    position: Point;
    playerId: number;
    turnsControlled: number;
    readonly board: Board;
    nextAction: ShipyardAction | undefined;
    constructor(shipyardId: string, shipCount: number, position: Point, playerId: number, turnsControlled: number, board: Board, nextAction: ShipyardAction | undefined);
    cloneToBoard(board: Board): Shipyard;
    setNextAction(action: ShipyardAction): void;
    get maxSpawn(): number;
    /**
     *  Returns the cell this shipyard is on.
     */
    get cell(): Cell;
    get player(): Player;
    /**
     * Converts a shipyard back to the normalized observation subset that constructed it.
     */
    observation(): number[];
}
