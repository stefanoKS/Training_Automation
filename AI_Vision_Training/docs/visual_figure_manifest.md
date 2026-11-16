# 図の出典と学習の問い / Visual figure manifest

SVG は編集可能な文字・図形です。PNG は同じ描画操作から作る PDF 用の代替です。
SVG uses editable text/shapes; PNG is a PDF fallback from the same drawing operations.

写真・保存済みモデル出力は再生成していません。streak_0005 の元記録はないため新しい数値図は省略しました。
Photos and saved model outputs were not regenerated. The new streak_0005 numeric figure is omitted: source records unavailable.

## 2026-11-16 clarity additions / 明確化の追加図

既存の正しいSVGと保存済み推論画像は変更していません。追加した静的図は3枚だけです。
`python assets\scripts\generate_clarity_figures.py` でこの3組だけを再生成します。
外部画像・配布フォント・ネットワークアクセスは使いません。PNGは同じ描画操作から作ります。

Existing correct SVGs and saved inference images are unchanged. Only three static diagrams are new.
Run `python assets\scripts\generate_clarity_figures.py` to regenerate these three pairs only.
They use no external images, distributed fonts or network access; PNGs use the same drawing operations.

| Asset / ID | Notebook / heading | Deterministic source | Provenance / limits | Preview | Learning question |
|---|---|---|---|---|---|
| `teach_fixed_fov_sampling` / V01 | Day01_02 / same field of view | `generate_clarity_figures.fixed_fov`, FIELD_MM/WIDTHS_PX/DEFECT_MM | Calculated synthetic; both full widths 1300 mm. Grid density/mark widths schematic, not to scale; no detection guarantee. | [SVG](../assets/svg/teach_fixed_fov_sampling.svg), [PNG](../assets/diagrams/teach_fixed_fov_sampling_svg.png) | 0.3 mmは何px？保存JPEGの拡大と再撮影は同じ？ / How many px span 0.3 mm? Is enlarging a JPEG recapture? |
| `teach_batch_first_pass` / V11 | Day04_02 / Stage 1 | `generate_clarity_figures.batch_first_pass`, computed IDs 0–63 | Calculated schematic; eight rows of eight images. No optimizer-update count claimed. | [SVG](../assets/svg/teach_batch_first_pass.svg), [PNG](../assets/diagrams/teach_batch_first_pass_svg.png) | batch=4なら一周に何batch？ / How many batches per pass at batch=4? |
| `teach_patch_overlap` / V13 | Day05_01 / analogy vs actual | `generate_clarity_figures.patch_overlap`, GRID_SIZE/REGIONS | Schematic overlapping supports; not actual resnet18 receptive-field dimensions or model output. | [SVG](../assets/svg/teach_patch_overlap.svg), [PNG](../assets/diagrams/teach_patch_overlap_svg.png) | 隣の特徴が同じ画素に依存する？ / Can adjacent features share input pixels? |

### 再利用・実行時の図 / Reused and live visuals

| Review IDs | Notebook / evidence | Source and disposition |
|---|---|---|
| V02 | Day01_02 / create→pixel→slice→6×6 | Existing pixel/slice SVGs remain unchanged; `clarity-slice-live` draws the executed 5×7 array and selected 3×3. |
| V03 | Day01_02 / resizing | Existing downsample and local-profile PNGs retained; no redundant dynamic widget. Existing live resize uses the lesson's own defect image. |
| V04 | Day02_02 / same five readings | Existing loop trace retained; live loop now prints signed difference, condition and verdict for each identical input. |
| V05 | Day02_02 / guided second pass | Existing branch visual plus bilingual parse→reject/log or tolerance text flow. |
| V06 | Day02_03 / BGR counterexample | `clarity-bgr-live`: calculated synthetic red/green/blue strip, wrong and corrected display, printed channel tuples. No external image. |
| V07 | Day02_03 / pixels→mask→contour | `clarity-mask-live`: calculated synthetic 7×8 source, exact mask, contour on the same mask; 12 white pixels vs 6 px². Existing pipeline retained. |
| V08 | Day03_01 / synchronized box forms | Existing correct bbox SVG; `clarity-bbox-live` computes both boxes: x2+24 gives centre (144,102), size (96,60). |
| V09 | Day03_02 / returned object→row | Existing result-object SVG; new adjacent text schema documents (N,4)/(N,)/(N,) and zero-row case. |
| V10 | Day03_03 / experiment sources | Table only: A toy, B archived52, C1 live640 cache, C2 live320 cache. Archived charts not regenerated. |
| V12 | Day04_03 / choose counting unit | Worked image-vs-box table precedes metrics; correct matching/confusion figures retained with original axes. |
| V14 | Day05_02 / score reading order | Adjacent bilingual annotation card for unchanged `ref_anomaly_panels.png`: historical raw21.439, mapMax21.762, normalized1.000, image threshold0.50. Not new inference. |
| V15 | Day05_03 / primary comparison protocol | Existing frozen-pipeline SVG moved to primary position; other overlap reduced, calibration controls moved before freeze. Archived five-column TEST panel opt-in after assessment; subsequent gallery explicitly CALIBRATION. |

The three new pairs passed deterministic generation, numeric/bounds tests and PNG inspection.
Live output is labelled calculated synthetic; archived model values are never presented as current computation.
New diagrams have no external licensing dependencies. Existing reference-image licenses/provenance remain unchanged.

## Existing source-checked figures / 既存の検証済み図

| Asset | Notebook section | Source code/data | Provenance | Preview | Learning question |
|---|---|---|---|---|---|
| `teach_code_cell_lifecycle.svg` | `00_Environment_Setup`: `Part 4` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_code_cell_lifecycle.svg) / [PNG](../assets/diagrams/teach_code_cell_lifecycle_svg.png) | 加算セルだけをもう一度実行すると、4 は何になりますか。 What happens to 4 if only the increment cell runs again? |
| `teach_pixel_inspector.svg` | `Day01_02_Pixels_and_Images`: `canvas = np.zeros` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_pixel_inspector.svg) / [PNG](../assets/diagrams/teach_pixel_inspector_svg.png) | canvas[2, 3] と canvas[3, 2] は同じですか。 Are canvas[2, 3] and canvas[3, 2] the same? |
| `teach_slice_walkthrough.svg` | `Day01_02_Pixels_and_Images`: `canvas = np.zeros` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_slice_walkthrough.svg) / [PNG](../assets/diagrams/teach_slice_walkthrough_svg.png) | [1:4, 2:5] の列の終点を 6 に変えると shape はどうなりますか。 What shape results if the column stop changes from 5 to 6? |
| `teach_cv_tasks_outputs.svg` | `Day01_03_Computer_Vision_Tasks`: `teach_cv_tasks_outputs.png` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_cv_tasks_outputs.svg) / [PNG](../assets/diagrams/teach_cv_tasks_outputs_svg.png) | マスクの画素数と四角の面積は等しいですか。 Does mask pixel count equal box area? |
| `teach_mass_units_chain.svg` | `Day02_01_Python_Basics`: `演習 2（中級）` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_mass_units_chain.svg) / [PNG](../assets/diagrams/teach_mass_units_chain_svg.png) | 厚さだけを2倍にすると、面積と重さはどう変わりますか。 If only thickness doubles, what happens to area and mass? |
| `teach_if_live_trace.svg` | `Day02_02_Conditions_Loops_Functions`: `measured_mm = 100.3` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_if_live_trace.svg) / [PNG](../assets/diagrams/teach_if_live_trace_svg.png) | 100.5001 mm に変えるとどちらの枝を通りますか。 Which branch runs for 100.5001 mm? |
| `teach_opencv_pixel_pipeline.svg` | `Day02_03_OpenCV_Image_Processing`: `Part 2` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_opencv_pixel_pipeline.svg) / [PNG](../assets/diagrams/teach_opencv_pixel_pipeline_svg.png) | 画素値がしきい値と等しいと、反転マスクでは何になりますか。 What does inverse threshold output when a pixel equals the threshold? |
| `teach_calibration_same_plane.svg` | `Day02_03_OpenCV_Image_Processing`: `calibrated_defects.png` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_calibration_same_plane.svg) / [PNG](../assets/diagrams/teach_calibration_same_plane_svg.png) | 倍率を2倍に仮定すると、同じ px² の mm² は何倍ですか。 If assumed px/mm doubles, how does the same px² convert to mm²? |
| `teach_bbox_one_example.svg` | `Day03_01_YOLO_Concepts`: `image_width, image_height = 240` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_bbox_one_example.svg) / [PNG](../assets/diagrams/teach_bbox_one_example_svg.png) | x2 だけを24 px増やすと中心と幅はどう変わりますか。 How do centre and width change if only x2 grows by 24 px? |
| `teach_yolo_result_object.svg` | `Day03_02_YOLO_Inference`: `Part 1` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_yolo_result_object.svg) / [PNG](../assets/diagrams/teach_yolo_result_object_svg.png) | 検出が0件なら、表には何行ありますか。 How many table rows are there when no box is detected? |
| `teach_epoch_batch_step.svg` | `Day04_02_YOLO_Training`: `EPOCHS = 15` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_epoch_batch_step.svg) / [PNG](../assets/diagrams/teach_epoch_batch_step_svg.png) | 64枚で batch=4 にすると、1 epoch のバッチ数はどうなりますか。 With 64 images and batch=4, how many batches make one epoch? |
| `teach_detection_matching.svg` | `Day04_03_YOLO_Evaluation`: `Part 3` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_detection_matching.svg) / [PNG](../assets/diagrams/teach_detection_matching_svg.png) | 1つの正解に予測が2つ重なると、両方がTPですか。 If two predictions overlap one truth box, are both TP? |
| `teach_patchcore_stages.svg` | `Day05_02_PatchCore_Training`: `model = Patchcore(` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_patchcore_stages.svg) / [PNG](../assets/diagrams/teach_patchcore_stages_svg.png) | 正常メモリに異常を入れると、距離による判定はどう変わりそうですか。 What could happen if anomalies enter the normal memory? |
| `teach_frozen_threshold_pipeline.svg` | `Day05_03_YOLO_vs_PatchCore`: `固定したしきい値で` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_frozen_threshold_pipeline.svg) / [PNG](../assets/diagrams/teach_frozen_threshold_pipeline_svg.png) | 試験結果を見て設定を変えたら、最終評価には何が必要ですか。 After tuning on test results, what is needed for a final evaluation? |
| `teach_group_split_vs_frame_split.svg` | `Day04_01_YOLO_Dataset_Annotation`: `import hashlib` | `generate_svg_figures.build_figure` / `teaching_data.py` | computed synthetic / schematic | [SVG](../assets/svg/teach_group_split_vs_frame_split.svg) / [PNG](../assets/diagrams/teach_group_split_vs_frame_split_svg.png) | 別のファイル形式なら SHA-256 が違っても独立した画像ですか。 Does a different SHA-256 after re-encoding prove independence? |

Source-checked values: box (96,72,168,132), image 240×240 -> YOLO 0 0.550 0.425 0.300 0.250; spot radius 9 px at (84,110), bounding edges from mask; pixel inspector selects only canvas[2,3]=100 in shape (5,7), with canvas[3,2]=0; slice walkthrough highlights rows 1..3 and columns 2..4, excludes stops 4/5, and draws canvas[1:4,2:5] = [[0,0,0],[0,100,0],[0,0,0]] with shape (3,3). 120 px / 100 mm = 1.2 px/mm; independent 60 px = 50 mm. Calibrated target contour areas: 475 / 925 px² -> 329.861111 / 642.361111 mm²; foreground pixel count is 1508, not the sum of geometric contour areas. Mass inputs match the unsolved exercise; its calculated answer is not inserted into exercise code.
