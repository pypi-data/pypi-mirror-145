import { Point } from "./Point";
export declare class Direction extends Point {
    static readonly NORTH: Direction;
    static readonly EAST: Direction;
    static readonly SOUTH: Direction;
    static readonly WEST: Direction;
    private constructor();
    equals(other: Direction): boolean;
    rotateLeft(): Direction;
    rotateRight(): Direction;
    opposite(): Direction;
    toChar(): string;
    toString(): string;
    toIndex(): number;
    static fromString(dirStr: string): Direction;
    static fromChar(dirChar: string): Direction;
    static fromIndex(index: number): Direction;
    static listDirections(): Direction[];
}
