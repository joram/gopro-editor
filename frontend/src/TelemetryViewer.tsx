import React, {useEffect, useRef, useState} from 'react';
import {
    CartesianGrid,
    Line,
    LineChart,
    ReferenceArea,
    ReferenceLine,
    ResponsiveContainer,
    XAxis,
    YAxis,
} from 'recharts';
import apiClient from "./api-client.ts";

interface Segment {
    start_time: number;
    end_time: number;
}

interface InterestPoint {
    timestamp: number;
    interest_level: number;
}

interface Props {
    videoUrl: string;
    projectSlug?: string;
    videoSlug?: string;
    interestData: InterestPoint[];
    suggestedSegments?: Segment[];
}

const CHART_TOP = 20;
const CHART_HEIGHT = 180;
const HANDLE_WIDTH = 14;
const MERGE_THRESHOLD = 1;

function insertAndMergeSegment(
    segments: Segment[],
    newSegment: Segment,
    threshold: number = MERGE_THRESHOLD
): Segment[] {
    const merged: Segment[] = [];
    let temp = { ...newSegment };

    for (const seg of segments) {
        if (temp.end_time + threshold < seg.start_time) {
            merged.push(temp);
            temp = seg;
        } else if (seg.end_time + threshold < temp.start_time) {
            merged.push(seg);
        } else {
            temp = {
                start_time: Math.min(temp.start_time, seg.start_time),
                end_time: Math.max(temp.end_time, seg.end_time),
            };
        }
    }

    merged.push(temp);
    return merged.sort((a, b) => a.start_time - b.start_time);
}

export const VideoWithInterestGraph: React.FC<Props> = ({
    videoUrl,
    interestData,
    suggestedSegments = [],
    projectSlug = "",
    videoSlug = "",
}) => {
    const videoRef = useRef<HTMLVideoElement>(null);
    const chartRef = useRef<any>(null);
    const [currentTime, setCurrentTime] = useState(0);
    const [segments, setSegments] = useState<Segment[]>(suggestedSegments);
    const [draftStart, setDraftStart] = useState<number | null>(null);
    const [contextMenu, setContextMenu] = useState<{ x: number; y: number; segmentIndex: number } | null>(null);
    const [dragging, setDragging] = useState<{ segmentIndex: number; edge: 'start' | 'end' } | null>(null);

    async function setAndSaveSegments(newSegments: Segment[]) {
        setSegments(newSegments);
        await apiClient.setSegments(projectSlug, videoSlug, newSegments);
    }
    useEffect(() => {
        const video = videoRef.current;
        const updateTime = () => setCurrentTime(video?.currentTime || 0);
        video?.addEventListener('timeupdate', updateTime);
        return () => video?.removeEventListener('timeupdate', updateTime);
    }, []);

    useEffect(() => {
        const handleMouseMove = async (e: MouseEvent) => {
            if (!dragging || !chartRef.current) return;
            const chartNode = chartRef.current.container as HTMLDivElement;
            const chartRect = chartNode.getBoundingClientRect();
            const xScale = (chartNode as any).__xScale;
            if (!xScale) return;

            const mouseX = e.clientX - chartRect.left;
            const newTime = xScale.invert(mouseX);


            const updated = [...segments];
            const seg = { ...updated[dragging.segmentIndex] };
            if (dragging.edge === 'start') {
                seg.start_time = Math.min(newTime, seg.end_time - 0.1);
            } else {
                seg.end_time = Math.max(newTime, seg.start_time + 0.1);
            }
            const cleaned = [...updated.slice(0, dragging.segmentIndex), ...updated.slice(dragging.segmentIndex + 1)];
            const newSegments = insertAndMergeSegment(cleaned, seg);
            await setAndSaveSegments(newSegments);
            return newSegments;
        };

        const stopDragging = () => setDragging(null);

        window.addEventListener('mousemove', handleMouseMove);
        window.addEventListener('mouseup', stopDragging);
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('mouseup', stopDragging);
        };
    }, [dragging]);

    useEffect(() => {
        const handleClickOutside = () => {
            if (contextMenu) setContextMenu(null);
        };
        window.addEventListener('click', handleClickOutside);
        return () => window.removeEventListener('click', handleClickOutside);
    }, [contextMenu]);

    const handleChartClick = async (e: any) => {
        if (!e || !e.activeLabel) return;
        const time = e.activeLabel;

        if (draftStart === null) {
            setDraftStart(time);
        } else {
            const newSegment = {
                start_time: Math.min(draftStart, time),
                end_time: Math.max(draftStart, time),
            };
            const newSegments = insertAndMergeSegment(segments, newSegment)
            await setAndSaveSegments(newSegments)
            setDraftStart(null);
        }
    };

    const handleChartMouseMove = (e: any) => {
        if (chartRef.current && e && e.chartX !== undefined) {
            const chartNode = chartRef.current.container as HTMLDivElement;
            chartNode && ((chartNode as any).__xScale = e.xAxis?.scale);
        }
    };

    return (
        <div style={{ position: 'relative' }}>
            <video ref={videoRef} src={videoUrl} controls width="100%" />
            <div style={{ width: '100%', height: 200, position: 'relative' }}>
                <ResponsiveContainer>
                    <LineChart
                        ref={chartRef}
                        data={interestData}
                        onClick={handleChartClick}
                        onMouseMove={handleChartMouseMove}
                    >
                        <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
                        <XAxis dataKey="timestamp" domain={['auto', 'auto']} type="number" />
                        <YAxis domain={[0, 'auto']} />
                        <Line type="monotone" dataKey="interest_level" stroke="#8884d8" dot={false} isAnimationActive={false} />
                        <ReferenceLine x={currentTime} stroke="red" strokeDasharray="3 3" label="Now" ifOverflow="extendDomain" />

                        {segments.map((seg, index) => (
                            <React.Fragment key={index}>
                                <ReferenceArea
                                    x1={seg.start_time}
                                    x2={seg.end_time}
                                    strokeOpacity={0}
                                    fill="rgba(0, 255, 0, 0.2)"
                                    onContextMenu={(e) => {
                                        e.preventDefault();
                                        setContextMenu({ x: e.clientX, y: e.clientY, segmentIndex: index });
                                    }}
                                />
                                <ReferenceLine x={seg.start_time} stroke="green" strokeWidth={3} strokeDasharray="4 2" ifOverflow="extendDomain" />
                                <ReferenceLine x={seg.end_time} stroke="green" strokeWidth={3} strokeDasharray="4 2" ifOverflow="extendDomain" />
                            </React.Fragment>
                        ))}

                        {draftStart !== null && (
                            <ReferenceLine x={draftStart} stroke="green" strokeDasharray="3 3" label="Start" />
                        )}
                    </LineChart>
                </ResponsiveContainer>

                {/* Drag handles */}
                {segments.map((seg, index) => {
                    const xScale = (chartRef.current?.container as any)?.__xScale;
                    if (!xScale) return null;
                    const left = xScale(seg.start_time);
                    const right = xScale(seg.end_time);

                    return (
                        <React.Fragment key={index}>
                            <div
                                onMouseDown={(e) => {
                                    e.stopPropagation();
                                    setDragging({ segmentIndex: index, edge: 'start' });
                                }}
                                style={{
                                    position: 'absolute',
                                    left: `${left - HANDLE_WIDTH / 2}px`,
                                    top: `${CHART_TOP}px`,
                                    width: `${HANDLE_WIDTH}px`,
                                    height: `${CHART_HEIGHT}px`,
                                    cursor: dragging?.segmentIndex === index ? 'grabbing' : 'grab',
                                    zIndex: 10,
                                }}
                            />
                            <div
                                onMouseDown={(e) => {
                                    e.stopPropagation();
                                    setDragging({ segmentIndex: index, edge: 'end' });
                                }}
                                style={{
                                    position: 'absolute',
                                    left: `${right - HANDLE_WIDTH / 2}px`,
                                    top: `${CHART_TOP}px`,
                                    width: `${HANDLE_WIDTH}px`,
                                    height: `${CHART_HEIGHT}px`,
                                    cursor: dragging?.segmentIndex === index ? 'grabbing' : 'grab',
                                    zIndex: 10,
                                }}
                            />
                        </React.Fragment>
                    );
                })}
            </div>

            {contextMenu && (
                <div
                    style={{
                        position: 'absolute',
                        top: contextMenu.y,
                        left: contextMenu.x,
                        backgroundColor: 'white',
                        border: '1px solid gray',
                        padding: '5px',
                        zIndex: 1000,
                        boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
                        cursor: 'pointer',
                    }}
                    onClick={async () => {
                        const updated = [...segments];
                        updated.splice(contextMenu.segmentIndex, 1);
                        await setAndSaveSegments(updated);
                        setContextMenu(null);
                    }}
                >
                    🗑 Delete segment
                </div>
            )}
        </div>
    );
};
