import { Board } from "./Board";
import { Fleet } from "./Fleet";
import { Point } from "./Point";
import { Shipyard } from "./Shipyard";
export declare class Cell {
    readonly position: Point;
    kore: number;
    shipyardId: string;
    fleetId: string;
    readonly board: Board;
    constructor(position: Point, kore: number, shipyardId: string, fleetId: string, board: Board);
    cloneToBoard(board: Board): Cell;
    get fleet(): Fleet | undefined;
    get shipyard(): Shipyard | undefined;
    neighbor(offset: Point): Cell;
    north(): Cell;
    south(): Cell;
    east(): Cell;
    west(): Cell;
}
