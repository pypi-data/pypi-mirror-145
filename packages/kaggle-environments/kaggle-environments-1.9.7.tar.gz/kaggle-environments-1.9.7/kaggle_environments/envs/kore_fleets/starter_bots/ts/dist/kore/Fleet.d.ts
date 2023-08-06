import { Board } from "./Board";
import { Cell } from "./Cell";
import { Direction } from "./Direction";
import { Player } from "./Player";
import { Point } from "./Point";
export declare class Fleet {
    readonly id: string;
    shipCount: number;
    direction: Direction;
    position: Point;
    flightPlan: string;
    kore: number;
    readonly playerId: number;
    readonly board: Board;
    constructor(fleetId: string, shipCount: number, direction: Direction, position: Point, kore: number, flightPlan: string, playerId: number, board: Board);
    cloneToBoard(board: Board): Fleet;
    get cell(): Cell;
    get player(): Player;
    get collectionRate(): number;
    /**
     * Returns the length of the longest possible flight plan this fleet can be assigned
     * @return
     */
    static maxFlightPlanLenForShipCount(shipCount: number): number;
    /**
     * Converts a fleet back to the normalized observation subset that constructed it.
     */
    observation(): string[];
    lessThanOtherAlliedFleet(other: Fleet): boolean;
}
