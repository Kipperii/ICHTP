import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Data provided by the user
data_str = """pair_id	img_a	img_b	stratum	is_pcg	pcg_seed	label	similarity_score	annotator	note	timestamp
1	scripts/test photo for similarity_label_tool/104.jpg	scripts/test photo for similarity_label_tool/47.jpg	same_dir	0	0	0	0.180132	K		2026-03-19T14:07:57
2	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/140.jpg	same_dir	0	0	0	0.256488	K		2026-03-19T14:08:14
3	scripts/test photo for similarity_label_tool/32.jpg	__PCG_GENERATED__	pcg_generated	1	42027654	2	0.346549	K		2026-03-19T14:08:18
4	scripts/test photo for similarity_label_tool/116.jpg	scripts/test photo for similarity_label_tool/47.jpg	same_dir	0	0	0	0.147227	K		2026-03-19T14:08:19
5	scripts/test photo for similarity_label_tool/173.jpg	scripts/test photo for similarity_label_tool/29.jpg	same_dir	0	0	0	0.186585	K		2026-03-19T14:08:19
6	scripts/test photo for similarity_label_tool/119.jpg	__PCG_GENERATED__	pcg_generated	1	42055182	1	0.326229	K		2026-03-19T14:08:23
7	scripts/test photo for similarity_label_tool/104.jpg	scripts/test photo for similarity_label_tool/113.jpg	same_dir	0	0	0	0.235624	K		2026-03-19T14:08:24
8	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/20.jpg	same_dir	0	0	0	0.242052	K		2026-03-19T14:08:24
9	scripts/test photo for similarity_label_tool/104.jpg	__PCG_GENERATED__	pcg_generated	1	42082710	1	0.405166	K		2026-03-19T14:08:28
10	scripts/test photo for similarity_label_tool/134.jpg	scripts/test photo for similarity_label_tool/27.jpg	same_dir	0	0	0	0.182033	K		2026-03-19T14:08:29
11	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/176.jpg	same_dir	0	0	0	0.269973	K		2026-03-19T14:08:30
12	scripts/test photo for similarity_label_tool/47.jpg	__PCG_GENERATED__	pcg_generated	1	42110238	2	0.470093	K		2026-03-19T14:08:32
13	scripts/test photo for similarity_label_tool/68.jpg	scripts/test photo for similarity_label_tool/8.jpg	same_dir	0	0	0	0.152529	K		2026-03-19T14:08:32
14	scripts/test photo for similarity_label_tool/50.jpg	scripts/test photo for similarity_label_tool/68.jpg	same_dir	0	0	0	0.155462	K		2026-03-19T14:08:34
15	scripts/test photo for similarity_label_tool/146.jpg	__PCG_GENERATED__	pcg_generated	1	42137766	3	0.359915	K		2026-03-19T14:08:39
16	scripts/test photo for similarity_label_tool/173.jpg	scripts/test photo for similarity_label_tool/38.jpg	same_dir	0	0	0	0.169184	K		2026-03-19T14:08:39
17	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/146.jpg	same_dir	0	0	0	0.349687	K		2026-03-19T14:08:42
18	scripts/test photo for similarity_label_tool/140.jpg	__PCG_GENERATED__	pcg_generated	1	42165294	1	0.340693	K		2026-03-19T14:08:44
19	scripts/test photo for similarity_label_tool/50.jpg	scripts/test photo for similarity_label_tool/95.jpg	same_dir	0	0	0	0.220343	K		2026-03-19T14:08:44
20	scripts/test photo for similarity_label_tool/113.jpg	scripts/test photo for similarity_label_tool/116.jpg	same_dir	0	0	2	0.452587	K		2026-03-19T14:08:47
21	scripts/test photo for similarity_label_tool/14.jpg	__PCG_GENERATED__	pcg_generated	1	42192822	2	0.336947	K		2026-03-19T14:08:48
22	scripts/test photo for similarity_label_tool/116.jpg	scripts/test photo for similarity_label_tool/161.jpg	same_dir	0	0	0	0.241735	K		2026-03-19T14:08:49
23	scripts/test photo for similarity_label_tool/143.jpg	scripts/test photo for similarity_label_tool/30.jpg	same_dir	0	0	0	0.237522	K		2026-03-19T14:08:50
24	scripts/test photo for similarity_label_tool/122.jpg	__PCG_GENERATED__	pcg_generated	1	42220350	1	0.339513	K		2026-03-19T14:08:51
25	scripts/test photo for similarity_label_tool/179.jpg	scripts/test photo for similarity_label_tool/44.jpg	same_dir	0	0	1	0.312154	K		2026-03-19T14:08:53
26	scripts/test photo for similarity_label_tool/89.jpg	scripts/test photo for similarity_label_tool/98.jpg	same_dir	0	0	0	0.138975	K		2026-03-19T14:08:54
27	scripts/test photo for similarity_label_tool/47.jpg	__PCG_GENERATED__	pcg_generated	1	42247878	2	0.493451	K		2026-03-19T14:08:56
28	scripts/test photo for similarity_label_tool/113.jpg	scripts/test photo for similarity_label_tool/27.jpg	same_dir	0	0	0	0.198834	K		2026-03-19T14:08:57
29	scripts/test photo for similarity_label_tool/32.jpg	scripts/test photo for similarity_label_tool/74.jpg	same_dir	0	0	0	0.210698	K		2026-03-19T14:08:58
30	scripts/test photo for similarity_label_tool/116.jpg	__PCG_GENERATED__	pcg_generated	1	42275406	1	0.232956	K		2026-03-19T14:08:59
31	scripts/test photo for similarity_label_tool/134.jpg	scripts/test photo for similarity_label_tool/28.jpg	same_dir	0	0	0	0.254276	K		2026-03-19T14:08:59
32	scripts/test photo for similarity_label_tool/107.jpg	scripts/test photo for similarity_label_tool/34.jpg	same_dir	0	0	0	0.168611	K		2026-03-19T14:09:00
33	scripts/test photo for similarity_label_tool/35.jpg	__PCG_GENERATED__	pcg_generated	1	42302934	2	0.573671	K		2026-03-19T14:09:02
34	scripts/test photo for similarity_label_tool/149.jpg	scripts/test photo for similarity_label_tool/56.jpg	same_dir	0	0	0	0.21366	K		2026-03-19T14:09:03
35	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/77.jpg	same_dir	0	0	0	0.221209	K		2026-03-19T14:09:04
36	scripts/test photo for similarity_label_tool/47.jpg	__PCG_GENERATED__	pcg_generated	1	42330462	2	0.429717	K		2026-03-19T14:09:05
37	scripts/test photo for similarity_label_tool/146.jpg	scripts/test photo for similarity_label_tool/167.jpg	same_dir	0	0	0	0.247748	K		2026-03-19T14:09:06
38	scripts/test photo for similarity_label_tool/128.jpg	scripts/test photo for similarity_label_tool/164.jpg	same_dir	0	0	0	0.270995	K		2026-03-19T14:09:09
39	scripts/test photo for similarity_label_tool/83.jpg	__PCG_GENERATED__	pcg_generated	1	42357990	2	0.366725	K		2026-03-19T14:09:12
40	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/34.jpg	same_dir	0	0	0	0.240876	K		2026-03-19T14:09:12
41	scripts/test photo for similarity_label_tool/38.jpg	scripts/test photo for similarity_label_tool/89.jpg	same_dir	0	0	0	0.211206	K		2026-03-19T14:09:13
42	scripts/test photo for similarity_label_tool/26.jpg	__PCG_GENERATED__	pcg_generated	1	42385518	3	0.403032	K		2026-03-19T14:09:18
43	scripts/test photo for similarity_label_tool/30.jpg	scripts/test photo for similarity_label_tool/32.jpg	same_dir	0	0	0	0.214007	K		2026-03-19T14:09:18
44	scripts/test photo for similarity_label_tool/26.jpg	scripts/test photo for similarity_label_tool/44.jpg	same_dir	0	0	0	0.20079	K		2026-03-19T14:09:19
45	scripts/test photo for similarity_label_tool/113.jpg	__PCG_GENERATED__	pcg_generated	1	42413046	1	0.253391	K		2026-03-19T14:09:20
46	scripts/test photo for similarity_label_tool/128.jpg	scripts/test photo for similarity_label_tool/179.jpg	same_dir	0	0	0	0.225549	K		2026-03-19T14:09:21
47	scripts/test photo for similarity_label_tool/146.jpg	scripts/test photo for similarity_label_tool/89.jpg	same_dir	0	0	0	0.244858	K		2026-03-19T14:09:21
48	scripts/test photo for similarity_label_tool/29.jpg	__PCG_GENERATED__	pcg_generated	1	42440574	1	0.238117	K		2026-03-19T14:09:25
49	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/35.jpg	same_dir	0	0	0	0.117468	K		2026-03-19T14:09:26
50	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/71.jpg	same_dir	0	0	0	0.219102	K		2026-03-19T14:09:27
51	scripts/test photo for similarity_label_tool/173.jpg	__PCG_GENERATED__	pcg_generated	1	42468102	1	0.181198	K		2026-03-19T14:09:28
52	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/68.jpg	same_dir	0	0	0	0.166859	K		2026-03-19T14:09:28
53	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/146.jpg	same_dir	0	0	1	0.29033	K		2026-03-19T14:09:32
54	scripts/test photo for similarity_label_tool/107.jpg	__PCG_GENERATED__	pcg_generated	1	42495630	3	0.309769	K		2026-03-19T14:09:34
55	scripts/test photo for similarity_label_tool/86.jpg	scripts/test photo for similarity_label_tool/92.jpg	same_dir	0	0	0	0.167021	K		2026-03-19T14:09:35
56	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/33.jpg	same_dir	0	0	0	0.228628	K		2026-03-19T14:09:36
57	scripts/test photo for similarity_label_tool/104.jpg	__PCG_GENERATED__	pcg_generated	1	42523158	2	0.371184	K		2026-03-19T14:09:37
58	scripts/test photo for similarity_label_tool/17.jpg	scripts/test photo for similarity_label_tool/80.jpg	same_dir	0	0	0	0.230309	K		2026-03-19T14:09:38
59	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/143.jpg	same_dir	0	0	1	0.345594	K		2026-03-19T14:09:41
60	scripts/test photo for similarity_label_tool/113.jpg	__PCG_GENERATED__	pcg_generated	1	42550686	1	0.559292	K		2026-03-19T14:09:42
61	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/47.jpg	same_dir	0	0	1	0.267279	K		2026-03-19T14:09:46
62	scripts/test photo for similarity_label_tool/29.jpg	scripts/test photo for similarity_label_tool/47.jpg	same_dir	0	0	0	0.156649	K		2026-03-19T14:09:47
63	scripts/test photo for similarity_label_tool/137.jpg	__PCG_GENERATED__	pcg_generated	1	42578214	1	0.282913	K		2026-03-19T14:09:49
64	scripts/test photo for similarity_label_tool/29.jpg	scripts/test photo for similarity_label_tool/83.jpg	same_dir	0	0	0	0.227753	K		2026-03-19T14:09:50
65	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/164.jpg	same_dir	0	0	0	0.230005	K		2026-03-19T14:09:50
66	scripts/test photo for similarity_label_tool/14.jpg	__PCG_GENERATED__	pcg_generated	1	42605742	2	0.288233	K		2026-03-19T14:09:54
67	scripts/test photo for similarity_label_tool/185.jpg	scripts/test photo for similarity_label_tool/20.jpg	same_dir	0	0	0	0.181231	K		2026-03-19T14:09:55
68	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/50.jpg	same_dir	0	0	0	0.226739	K		2026-03-19T14:09:56
69	scripts/test photo for similarity_label_tool/20.jpg	__PCG_GENERATED__	pcg_generated	1	42633270	3	0.563757	K		2026-03-19T14:09:59
70	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/32.jpg	same_dir	0	0	0	0.225327	K		2026-03-19T14:10:00
71	scripts/test photo for similarity_label_tool/35.jpg	scripts/test photo for similarity_label_tool/65.jpg	same_dir	0	0	0	0.223006	K		2026-03-19T14:10:01
72	scripts/test photo for similarity_label_tool/30.jpg	__PCG_GENERATED__	pcg_generated	1	42660798	2	0.461813	K		2026-03-19T14:10:03
73	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/30.jpg	same_dir	0	0	0	0.211886	K		2026-03-19T14:10:04
74	scripts/test photo for similarity_label_tool/167.jpg	scripts/test photo for similarity_label_tool/30.jpg	same_dir	0	0	0	0.237507	K		2026-03-19T14:10:05
75	scripts/test photo for similarity_label_tool/104.jpg	__PCG_GENERATED__	pcg_generated	1	42688326	2	0.456851	K		2026-03-19T14:10:06
76	scripts/test photo for similarity_label_tool/143.jpg	scripts/test photo for similarity_label_tool/23.jpg	same_dir	0	0	0	0.164833	K		2026-03-19T14:10:07
77	scripts/test photo for similarity_label_tool/35.jpg	scripts/test photo for similarity_label_tool/44.jpg	same_dir	0	0	0	0.135658	K		2026-03-19T14:10:08
78	scripts/test photo for similarity_label_tool/27.jpg	__PCG_GENERATED__	pcg_generated	1	42715854	3	0.428597	K		2026-03-19T14:10:10
79	scripts/test photo for similarity_label_tool/35.jpg	scripts/test photo for similarity_label_tool/80.jpg	same_dir	0	0	0	0.210685	K		2026-03-19T14:10:11
80	scripts/test photo for similarity_label_tool/33.jpg	scripts/test photo for similarity_label_tool/56.jpg	same_dir	0	0	0	0.483089	K		2026-03-19T14:10:12
81	scripts/test photo for similarity_label_tool/134.jpg	__PCG_GENERATED__	pcg_generated	1	42743382	2	0.43882	K		2026-03-19T14:10:21
82	scripts/test photo for similarity_label_tool/119.jpg	scripts/test photo for similarity_label_tool/149.jpg	same_dir	0	0	0	0.200998	K		2026-03-19T14:10:21
83	scripts/test photo for similarity_label_tool/44.jpg	scripts/test photo for similarity_label_tool/95.jpg	same_dir	0	0	0	0.225529	K		2026-03-19T14:10:22
84	scripts/test photo for similarity_label_tool/41.jpg	__PCG_GENERATED__	pcg_generated	1	42770910	2	0.470218	K		2026-03-19T14:10:23
85	scripts/test photo for similarity_label_tool/20.jpg	scripts/test photo for similarity_label_tool/98.jpg	same_dir	0	0	0	0.226426	K		2026-03-19T14:10:24
86	scripts/test photo for similarity_label_tool/20.jpg	scripts/test photo for similarity_label_tool/86.jpg	same_dir	0	0	0	0.248391	K		2026-03-19T14:10:25
87	scripts/test photo for similarity_label_tool/33.jpg	__PCG_GENERATED__	pcg_generated	1	42798438	1	0.445273	K		2026-03-19T14:10:26
88	scripts/test photo for similarity_label_tool/32.jpg	scripts/test photo for similarity_label_tool/8.jpg	same_dir	0	0	0	0.138512	K		2026-03-19T14:10:27
89	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/164.jpg	same_dir	0	0	1	0.27608	K		2026-03-19T14:10:28
90	scripts/test photo for similarity_label_tool/38.jpg	__PCG_GENERATED__	pcg_generated	1	42825966	2	0.388006	K		2026-03-19T14:10:30
91	scripts/test photo for similarity_label_tool/26.jpg	scripts/test photo for similarity_label_tool/95.jpg	same_dir	0	0	0	0.219216	K		2026-03-19T14:10:31
92	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/30.jpg	same_dir	0	0	0	0.195165	K		2026-03-19T14:10:32
93	scripts/test photo for similarity_label_tool/26.jpg	__PCG_GENERATED__	pcg_generated	1	42853494	2	0.332558	K		2026-03-19T14:10:41
94	scripts/test photo for similarity_label_tool/104.jpg	scripts/test photo for similarity_label_tool/119.jpg	same_dir	0	0	0	0.233188	K		2026-03-19T14:10:42
95	scripts/test photo for similarity_label_tool/74.jpg	scripts/test photo for similarity_label_tool/80.jpg	same_dir	0	0	0	0.204863	K		2026-03-19T14:10:43
96	scripts/test photo for similarity_label_tool/170.jpg	__PCG_GENERATED__	pcg_generated	1	42881022	3	0.600551	K		2026-03-19T14:10:44
97	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/140.jpg	same_dir	0	0	0	0.249608	K		2026-03-19T14:10:45
98	scripts/test photo for similarity_label_tool/28.jpg	scripts/test photo for similarity_label_tool/80.jpg	same_dir	0	0	0	0.208104	K		2026-03-19T14:10:46
99	scripts/test photo for similarity_label_tool/14.jpg	__PCG_GENERATED__	pcg_generated	1	42908550	1	0.329155	K		2026-03-19T14:10:49
100	scripts/test photo for similarity_label_tool/113.jpg	scripts/test photo for similarity_label_tool/44.jpg	same_dir	0	0	0	0.177476	K		2026-03-19T14:10:50
101	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/71.jpg	same_dir	0	0	0	0.214695	K		2026-03-19T14:10:50
102	scripts/test photo for similarity_label_tool/176.jpg	__PCG_GENERATED__	pcg_generated	1	42936078	2	0.336062	K		2026-03-19T14:10:52
103	scripts/test photo for similarity_label_tool/122.jpg	scripts/test photo for similarity_label_tool/34.jpg	same_dir	0	0	0	0.224277	K		2026-03-19T14:10:53
104	scripts/test photo for similarity_label_tool/27.jpg	scripts/test photo for similarity_label_tool/92.jpg	same_dir	0	0	0	0.190916	K		2026-03-19T14:10:54
105	scripts/test photo for similarity_label_tool/29.jpg	__PCG_GENERATED__	pcg_generated	1	42963606	2	0.276892	K		2026-03-19T14:10:56
106	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/95.jpg	same_dir	0	0	0	0.247755	K		2026-03-19T14:10:57
107	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/41.jpg	same_dir	0	0	1	0.322395	K		2026-03-19T14:11:02
108	scripts/test photo for similarity_label_tool/146.jpg	__PCG_GENERATED__	pcg_generated	1	42991134	1	0.236464	K		2026-03-19T14:11:05
109	scripts/test photo for similarity_label_tool/33.jpg	scripts/test photo for similarity_label_tool/34.jpg	same_dir	0	0	0	0.146618	K		2026-03-19T14:11:07
110	scripts/test photo for similarity_label_tool/176.jpg	scripts/test photo for similarity_label_tool/83.jpg	same_dir	0	0	0	0.205243	K		2026-03-19T14:11:09
111	scripts/test photo for similarity_label_tool/68.jpg	__PCG_GENERATED__	pcg_generated	1	43018662	0	0.268325	K		2026-03-19T14:11:11
112	scripts/test photo for similarity_label_tool/119.jpg	scripts/test photo for similarity_label_tool/140.jpg	same_dir	0	0	1	0.273112	K		2026-03-19T14:11:16
113	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/158.jpg	same_dir	0	0	0	0.213721	K		2026-03-19T14:11:17
114	scripts/test photo for similarity_label_tool/8.jpg	__PCG_GENERATED__	pcg_generated	1	43046190	1	0.187028	K		2026-03-19T14:11:19
115	scripts/test photo for similarity_label_tool/27.jpg	scripts/test photo for similarity_label_tool/29.jpg	same_dir	0	0	0	0.145607	K		2026-03-19T14:11:20
116	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/29.jpg	same_dir	0	0	0	0.228649	K		2026-03-19T14:11:20
117	scripts/test photo for similarity_label_tool/101.jpg	__PCG_GENERATED__	pcg_generated	1	43073718	3	0.626599	K		2026-03-19T14:11:23
118	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/41.jpg	same_dir	0	0	0	0.227256	K		2026-03-19T14:11:24
119	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/14.jpg	same_dir	0	0	0	0.2374	K		2026-03-19T14:11:24
120	scripts/test photo for similarity_label_tool/50.jpg	__PCG_GENERATED__	pcg_generated	1	43101246	2	0.377685	K		2026-03-19T14:11:29
121	scripts/test photo for similarity_label_tool/158.jpg	scripts/test photo for similarity_label_tool/8.jpg	same_dir	0	0	0	0.209702	K		2026-03-19T14:11:30
122	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/20.jpg	same_dir	0	0	0	0.201359	K		2026-03-19T14:11:31
123	scripts/test photo for similarity_label_tool/68.jpg	__PCG_GENERATED__	pcg_generated	1	43128774	2	0.321282	K		2026-03-19T14:11:35
124	scripts/test photo for similarity_label_tool/185.jpg	scripts/test photo for similarity_label_tool/34.jpg	same_dir	0	0	0	0.23366	K		2026-03-19T14:11:35
125	scripts/test photo for similarity_label_tool/122.jpg	scripts/test photo for similarity_label_tool/26.jpg	same_dir	0	0	0	0.198044	K		2026-03-19T14:11:36
126	scripts/test photo for similarity_label_tool/128.jpg	__PCG_GENERATED__	pcg_generated	1	43156302	2	0.376106	K		2026-03-19T14:11:41
127	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/65.jpg	same_dir	0	0	0	0.25324	K		2026-03-19T14:11:42
128	scripts/test photo for similarity_label_tool/170.jpg	scripts/test photo for similarity_label_tool/68.jpg	same_dir	0	0	0	0.24187	K		2026-03-19T14:11:43
129	scripts/test photo for similarity_label_tool/38.jpg	__PCG_GENERATED__	pcg_generated	1	43183830	2	0.340141	K		2026-03-19T14:11:46
130	scripts/test photo for similarity_label_tool/116.jpg	scripts/test photo for similarity_label_tool/34.jpg	same_dir	0	0	0	0.22312	K		2026-03-19T14:11:46
131	scripts/test photo for similarity_label_tool/161.jpg	scripts/test photo for similarity_label_tool/173.jpg	same_dir	0	0	1	0.337733	K		2026-03-19T14:11:49
132	scripts/test photo for similarity_label_tool/173.jpg	__PCG_GENERATED__	pcg_generated	1	43211358	1	0.249995	K		2026-03-19T14:11:52
133	scripts/test photo for similarity_label_tool/179.jpg	scripts/test photo for similarity_label_tool/8.jpg	same_dir	0	0	0	0.242409	K		2026-03-19T14:11:53
134	scripts/test photo for similarity_label_tool/33.jpg	scripts/test photo for similarity_label_tool/35.jpg	same_dir	0	0	0	0.189351	K		2026-03-19T14:11:53
135	scripts/test photo for similarity_label_tool/158.jpg	__PCG_GENERATED__	pcg_generated	1	43238886	2	0.287254	K		2026-03-19T14:11:59
136	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/17.jpg	same_dir	0	0	0	0.238065	K		2026-03-19T14:12:00
137	scripts/test photo for similarity_label_tool/134.jpg	scripts/test photo for similarity_label_tool/140.jpg	same_dir	0	0	2	0.361609	K		2026-03-19T14:12:03
138	scripts/test photo for similarity_label_tool/146.jpg	__PCG_GENERATED__	pcg_generated	1	43266414	1	0.340868	K		2026-03-19T14:12:05
139	scripts/test photo for similarity_label_tool/176.jpg	scripts/test photo for similarity_label_tool/26.jpg	same_dir	0	0	0	0.240604	K		2026-03-19T14:12:06
140	scripts/test photo for similarity_label_tool/131.jpg	scripts/test photo for similarity_label_tool/173.jpg	same_dir	0	0	1	0.199726	K		2026-03-19T14:12:08
141	scripts/test photo for similarity_label_tool/125.jpg	__PCG_GENERATED__	pcg_generated	1	43293942	3	0.490114	K		2026-03-19T14:12:09
142	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/179.jpg	same_dir	0	0	1	0.338245	K		2026-03-19T14:12:11
143	scripts/test photo for similarity_label_tool/176.jpg	scripts/test photo for similarity_label_tool/68.jpg	same_dir	0	0	0	0.206854	K		2026-03-19T14:12:12
144	scripts/test photo for similarity_label_tool/137.jpg	__PCG_GENERATED__	pcg_generated	1	43321470	3	0.530269	K		2026-03-19T14:12:14
145	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/33.jpg	same_dir	0	0	0	0.195282	K		2026-03-19T14:12:15
146	scripts/test photo for similarity_label_tool/113.jpg	scripts/test photo for similarity_label_tool/98.jpg	same_dir	0	0	0	0.223929	K		2026-03-19T14:12:16
147	scripts/test photo for similarity_label_tool/95.jpg	__PCG_GENERATED__	pcg_generated	1	43348998	2	0.423072	K		2026-03-19T14:12:22
148	scripts/test photo for similarity_label_tool/128.jpg	scripts/test photo for similarity_label_tool/170.jpg	same_dir	0	0	1	0.264773	K		2026-03-19T14:12:23
149	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/182.jpg	same_dir	0	0	1	0.380302	K		2026-03-19T14:12:24
150	scripts/test photo for similarity_label_tool/50.jpg	__PCG_GENERATED__	pcg_generated	1	43376526	0	0.255168	K		2026-03-19T14:12:26
151	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/83.jpg	same_dir	0	0	2	0.345429	K		2026-03-19T14:12:29
152	scripts/test photo for similarity_label_tool/101.jpg	scripts/test photo for similarity_label_tool/167.jpg	same_dir	0	0	1	0.297537	K		2026-03-19T14:12:30
153	scripts/test photo for similarity_label_tool/158.jpg	__PCG_GENERATED__	pcg_generated	1	43404054	1	0.199483	K		2026-03-19T14:12:33
154	scripts/test photo for similarity_label_tool/143.jpg	scripts/test photo for similarity_label_tool/89.jpg	same_dir	0	0	0	0.24824	K		2026-03-19T14:12:34
155	scripts/test photo for similarity_label_tool/149.jpg	scripts/test photo for similarity_label_tool/173.jpg	same_dir	0	0	0	0.156015	K		2026-03-19T14:12:35
156	scripts/test photo for similarity_label_tool/116.jpg	__PCG_GENERATED__	pcg_generated	1	43431582	2	0.288269	K		2026-03-19T14:12:36
157	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/134.jpg	same_dir	0	0	2	0.431235	K		2026-03-19T14:12:39
158	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/47.jpg	same_dir	0	0	2	0.326918	K		2026-03-19T14:12:41
159	scripts/test photo for similarity_label_tool/113.jpg	__PCG_GENERATED__	pcg_generated	1	43459110	1	0.316056	K		2026-03-19T14:12:42
160	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/29.jpg	same_dir	0	0	0	0.227293	K		2026-03-19T14:12:43
161	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/95.jpg	same_dir	0	0	0	0.159778	K		2026-03-19T14:12:44
162	scripts/test photo for similarity_label_tool/167.jpg	__PCG_GENERATED__	pcg_generated	1	43486638	1	0.317865	K		2026-03-19T14:12:46
163	scripts/test photo for similarity_label_tool/131.jpg	scripts/test photo for similarity_label_tool/77.jpg	same_dir	0	0	0	0.215013	K		2026-03-19T14:12:47
164	scripts/test photo for similarity_label_tool/119.jpg	scripts/test photo for similarity_label_tool/17.jpg	same_dir	0	0	0	0.197648	K		2026-03-19T14:12:48
165	scripts/test photo for similarity_label_tool/116.jpg	__PCG_GENERATED__	pcg_generated	1	43514166	1	0.281607	K		2026-03-19T14:12:49
166	scripts/test photo for similarity_label_tool/29.jpg	scripts/test photo for similarity_label_tool/30.jpg	same_dir	0	0	0	0.227202	K		2026-03-19T14:12:49
167	scripts/test photo for similarity_label_tool/113.jpg	scripts/test photo for similarity_label_tool/31.jpg	same_dir	0	0	0	0.246027	K		2026-03-19T14:12:50
168	scripts/test photo for similarity_label_tool/161.jpg	__PCG_GENERATED__	pcg_generated	1	43541694	1	0.336011	K		2026-03-19T14:12:52
169	scripts/test photo for similarity_label_tool/29.jpg	scripts/test photo for similarity_label_tool/34.jpg	same_dir	0	0	0	0.213986	K		2026-03-19T14:12:52
170	scripts/test photo for similarity_label_tool/34.jpg	scripts/test photo for similarity_label_tool/41.jpg	same_dir	0	0	0	0.218193	K		2026-03-19T14:12:53
171	scripts/test photo for similarity_label_tool/77.jpg	__PCG_GENERATED__	pcg_generated	1	43569222	3	0.666766	K		2026-03-19T14:12:55
172	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/143.jpg	same_dir	0	0	2	0.522079	K		2026-03-19T14:12:57
173	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/179.jpg	same_dir	0	0	1	0.274092	K		2026-03-19T14:12:58
174	scripts/test photo for similarity_label_tool/161.jpg	__PCG_GENERATED__	pcg_generated	1	43596750	1	0.31632	K		2026-03-19T14:12:59
175	scripts/test photo for similarity_label_tool/50.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	0	0.209665	K		2026-03-19T14:13:00
176	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	0	0.265516	K		2026-03-19T14:13:02
177	scripts/test photo for similarity_label_tool/30.jpg	__PCG_GENERATED__	pcg_generated	1	43624278	0	0.234679	K		2026-03-19T14:13:03
178	scripts/test photo for similarity_label_tool/101.jpg	scripts/test photo for similarity_label_tool/179.jpg	random	0	0	0	0.25039	K		2026-03-19T14:13:04
179	scripts/test photo for similarity_label_tool/28.jpg	scripts/test photo for similarity_label_tool/31.jpg	random	0	0	0	0.169159	K		2026-03-19T14:13:04
180	scripts/test photo for similarity_label_tool/143.jpg	__PCG_GENERATED__	pcg_generated	1	43651806	3	0.568872	K		2026-03-19T14:13:09
181	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/116.jpg	random	0	0	0	0.224028	K		2026-03-19T14:14:01
182	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/26.jpg	random	0	0	0	0.222354	K		2026-03-19T14:14:03
183	scripts/test photo for similarity_label_tool/68.jpg	__PCG_GENERATED__	pcg_generated	1	43679334	3	0.38566	K		2026-03-19T14:14:04
184	scripts/test photo for similarity_label_tool/143.jpg	scripts/test photo for similarity_label_tool/20.jpg	random	0	0	0	0.178328	K		2026-03-19T14:14:05
185	scripts/test photo for similarity_label_tool/122.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	0	0.20364	K		2026-03-19T14:14:06
186	scripts/test photo for similarity_label_tool/107.jpg	__PCG_GENERATED__	pcg_generated	1	43706862	1	0.312144	K		2026-03-19T14:14:07
187	scripts/test photo for similarity_label_tool/161.jpg	scripts/test photo for similarity_label_tool/80.jpg	random	0	0	1	0.292809	K		2026-03-19T14:14:08
188	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/80.jpg	random	0	0	0	0.278766	K		2026-03-19T14:14:10
189	scripts/test photo for similarity_label_tool/44.jpg	__PCG_GENERATED__	pcg_generated	1	43734390	2	0.346239	K		2026-03-19T14:14:12
190	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/164.jpg	random	0	0	0	0.259945	K		2026-03-19T14:14:14
191	scripts/test photo for similarity_label_tool/128.jpg	scripts/test photo for similarity_label_tool/149.jpg	random	0	0	0	0.176516	K		2026-03-19T14:14:15
192	scripts/test photo for similarity_label_tool/179.jpg	__PCG_GENERATED__	pcg_generated	1	43761918	1	0.333874	K		2026-03-19T14:14:17
193	scripts/test photo for similarity_label_tool/176.jpg	scripts/test photo for similarity_label_tool/74.jpg	random	0	0	0	0.204893	K		2026-03-19T14:14:18
194	scripts/test photo for similarity_label_tool/26.jpg	scripts/test photo for similarity_label_tool/41.jpg	random	0	0	0	0.196457	K		2026-03-19T14:14:19
195	scripts/test photo for similarity_label_tool/26.jpg	__PCG_GENERATED__	pcg_generated	1	43789446	1	0.323475	K		2026-03-19T14:14:20
196	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/31.jpg	random	0	0	0	0.174025	K		2026-03-19T14:14:20
197	scripts/test photo for similarity_label_tool/68.jpg	scripts/test photo for similarity_label_tool/98.jpg	random	0	0	0	0.207492	K		2026-03-19T14:14:21
198	scripts/test photo for similarity_label_tool/119.jpg	__PCG_GENERATED__	pcg_generated	1	43816974	1	0.345596	K		2026-03-19T14:14:22
199	scripts/test photo for similarity_label_tool/23.jpg	scripts/test photo for similarity_label_tool/33.jpg	random	0	0	0	0.180168	K		2026-03-19T14:14:23
200	scripts/test photo for similarity_label_tool/101.jpg	scripts/test photo for similarity_label_tool/34.jpg	random	0	0	0	0.184057	K		2026-03-19T14:14:23
201	scripts/test photo for similarity_label_tool/98.jpg	__PCG_GENERATED__	pcg_generated	1	43844502	1	0.275444	K		2026-03-19T14:14:27
202	scripts/test photo for similarity_label_tool/27.jpg	scripts/test photo for similarity_label_tool/71.jpg	random	0	0	0	0.194215	K		2026-03-19T14:14:27
203	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	0	0.193467	K		2026-03-19T14:14:28
204	scripts/test photo for similarity_label_tool/89.jpg	__PCG_GENERATED__	pcg_generated	1	43872030	3	0.334002	K		2026-03-19T14:14:29
205	scripts/test photo for similarity_label_tool/80.jpg	scripts/test photo for similarity_label_tool/92.jpg	random	0	0	0	0.175978	K		2026-03-19T14:14:30
206	scripts/test photo for similarity_label_tool/122.jpg	scripts/test photo for similarity_label_tool/143.jpg	random	0	0	1	0.266301	K		2026-03-19T14:14:31
207	scripts/test photo for similarity_label_tool/167.jpg	__PCG_GENERATED__	pcg_generated	1	43899558	2	0.665139	K		2026-03-19T14:14:34
208	scripts/test photo for similarity_label_tool/119.jpg	scripts/test photo for similarity_label_tool/80.jpg	random	0	0	0	0.207636	K		2026-03-19T14:14:34
209	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/27.jpg	random	0	0	0	0.19468	K		2026-03-19T14:14:35
210	scripts/test photo for similarity_label_tool/113.jpg	__PCG_GENERATED__	pcg_generated	1	43927086	2	0.415395	K		2026-03-19T14:14:36
211	scripts/test photo for similarity_label_tool/146.jpg	scripts/test photo for similarity_label_tool/149.jpg	random	0	0	1	0.288818	K		2026-03-19T14:14:41
212	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/30.jpg	random	0	0	0	0.244168	K		2026-03-19T14:14:41
213	scripts/test photo for similarity_label_tool/27.jpg	__PCG_GENERATED__	pcg_generated	1	43954614	3	0.607187	K		2026-03-19T14:14:43
214	scripts/test photo for similarity_label_tool/158.jpg	scripts/test photo for similarity_label_tool/41.jpg	random	0	0	2	0.3617	K		2026-03-19T14:14:46
215	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/35.jpg	random	0	0	0	0.208601	K		2026-03-19T14:14:47
216	scripts/test photo for similarity_label_tool/149.jpg	__PCG_GENERATED__	pcg_generated	1	43982142	1	0.206289	K		2026-03-19T14:14:48
217	scripts/test photo for similarity_label_tool/32.jpg	scripts/test photo for similarity_label_tool/77.jpg	random	0	0	0	0.215783	K		2026-03-19T14:14:49
218	scripts/test photo for similarity_label_tool/143.jpg	scripts/test photo for similarity_label_tool/185.jpg	random	0	0	1	0.334801	K		2026-03-19T14:14:51
219	scripts/test photo for similarity_label_tool/74.jpg	__PCG_GENERATED__	pcg_generated	1	44009670	0	0.25714	K		2026-03-19T14:14:53
220	scripts/test photo for similarity_label_tool/83.jpg	scripts/test photo for similarity_label_tool/86.jpg	random	0	0	2	0.497864	K		2026-03-19T14:14:54
221	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/77.jpg	random	0	0	0	0.215964	K		2026-03-19T14:14:55
222	scripts/test photo for similarity_label_tool/32.jpg	__PCG_GENERATED__	pcg_generated	1	44037198	1	0.472867	K		2026-03-19T14:14:56
223	scripts/test photo for similarity_label_tool/113.jpg	scripts/test photo for similarity_label_tool/32.jpg	random	0	0	0	0.238965	K		2026-03-19T14:14:56
224	scripts/test photo for similarity_label_tool/173.jpg	scripts/test photo for similarity_label_tool/74.jpg	random	0	0	0	0.191276	K		2026-03-19T14:14:57
225	scripts/test photo for similarity_label_tool/31.jpg	__PCG_GENERATED__	pcg_generated	1	44064726	3	0.495183	K		2026-03-19T14:14:58
226	scripts/test photo for similarity_label_tool/107.jpg	scripts/test photo for similarity_label_tool/146.jpg	random	0	0	1	0.295661	K		2026-03-19T14:14:50
227	scripts/test photo for similarity_label_tool/101.jpg	scripts/test photo for similarity_label_tool/158.jpg	random	0	0	0	0.236206	K		2026-03-19T14:15:01
228	scripts/test photo for similarity_label_tool/80.jpg	__PCG_GENERATED__	pcg_generated	1	44092254	2	0.298191	K		2026-03-19T14:15:02
229	scripts/test photo for similarity_label_tool/122.jpg	scripts/test photo for similarity_label_tool/56.jpg	random	0	0	0	0.191574	K		2026-03-19T14:15:02
230	scripts/test photo for similarity_label_tool/32.jpg	scripts/test photo for similarity_label_tool/98.jpg	random	0	0	0	0.21042	K		2026-03-19T14:15:03
231	scripts/test photo for similarity_label_tool/8.jpg	__PCG_GENERATED__	pcg_generated	1	44119782	3	0.665095	K		2026-03-19T14:15:07
232	scripts/test photo for similarity_label_tool/128.jpg	scripts/test photo for similarity_label_tool/143.jpg	random	0	0	1	0.340633	K		2026-03-19T14:15:10
233	scripts/test photo for similarity_label_tool/176.jpg	scripts/test photo for similarity_label_tool/47.jpg	random	0	0	1	0.315505	K		2026-03-19T14:15:12
234	scripts/test photo for similarity_label_tool/164.jpg	__PCG_GENERATED__	pcg_generated	1	44147310	1	0.300464	K		2026-03-19T14:15:14
235	scripts/test photo for similarity_label_tool/27.jpg	scripts/test photo for similarity_label_tool/41.jpg	random	0	0	0	0.190899	K		2026-03-19T14:15:15
236	scripts/test photo for similarity_label_tool/173.jpg	scripts/test photo for similarity_label_tool/27.jpg	random	0	0	0	0.146256	K		2026-03-19T14:15:16
237	scripts/test photo for similarity_label_tool/28.jpg	__PCG_GENERATED__	pcg_generated	1	44174838	3	0.273011	K		2026-03-19T14:15:18
238	scripts/test photo for similarity_label_tool/101.jpg	scripts/test photo for similarity_label_tool/119.jpg	random	0	0	0	0.218654	K		2026-03-19T14:15:23
239	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/92.jpg	random	0	0	1	0.252773	K		2026-03-19T14:15:24
240	scripts/test photo for similarity_label_tool/134.jpg	__PCG_GENERATED__	pcg_generated	1	44202366	1	0.540587	K		2026-03-19T14:15:24
241	scripts/test photo for similarity_label_tool/38.jpg	scripts/test photo for similarity_label_tool/80.jpg	random	0	0	0	0.211752	K		2026-03-19T14:15:25
242	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.231624	K		2026-03-19T14:15:26
243	scripts/test photo for similarity_label_tool/41.jpg	__PCG_GENERATED__	pcg_generated	1	44229894	1	0.229928	K		2026-03-19T14:15:27
244	scripts/test photo for similarity_label_tool/107.jpg	scripts/test photo for similarity_label_tool/26.jpg	random	0	0	0	0.239361	K		2026-03-19T14:15:28
245	scripts/test photo for similarity_label_tool/164.jpg	scripts/test photo for similarity_label_tool/74.jpg	random	0	0	0	0.246161	K		2026-03-19T14:15:28
246	scripts/test photo for similarity_label_tool/110.jpg	__PCG_GENERATED__	pcg_generated	1	44257422	1	0.429276	K		2026-03-19T14:15:29
247	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/173.jpg	random	0	0	1	0.221729	K		2026-03-19T14:15:30
248	scripts/test photo for similarity_label_tool/107.jpg	scripts/test photo for similarity_label_tool/122.jpg	random	0	0	0	0.238587	K		2026-03-19T14:15:32
249	scripts/test photo for similarity_label_tool/107.jpg	__PCG_GENERATED__	pcg_generated	1	44284950	3	0.701367	K		2026-03-19T14:15:34
250	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/164.jpg	random	0	0	0	0.199644	K		2026-03-19T14:15:37
251	scripts/test photo for similarity_label_tool/83.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	1	0.500443	K		2026-03-19T14:15:39
252	scripts/test photo for similarity_label_tool/34.jpg	__PCG_GENERATED__	pcg_generated	1	44312478	2	0.377665	K		2026-03-19T14:15:42
253	scripts/test photo for similarity_label_tool/65.jpg	scripts/test photo for similarity_label_tool/98.jpg	random	0	0	0	0.173229	K		2026-03-19T14:15:43
254	scripts/test photo for similarity_label_tool/107.jpg	scripts/test photo for similarity_label_tool/8.jpg	random	0	0	0	0.246143	K		2026-03-19T14:15:43
255	scripts/test photo for similarity_label_tool/14.jpg	__PCG_GENERATED__	pcg_generated	1	44340006	2	0.339505	K		2026-03-19T14:15:44
256	scripts/test photo for similarity_label_tool/161.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	1	0.29888	K		2026-03-19T14:15:46
257	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/34.jpg	random	0	0	0	0.246621	K		2026-03-19T14:15:48
258	scripts/test photo for similarity_label_tool/56.jpg	__PCG_GENERATED__	pcg_generated	1	44367534	2	0.685785	K		2026-03-19T14:15:51
259	scripts/test photo for similarity_label_tool/27.jpg	scripts/test photo for similarity_label_tool/56.jpg	random	0	0	0	0.188103	K		2026-03-19T14:15:52
260	scripts/test photo for similarity_label_tool/8.jpg	scripts/test photo for similarity_label_tool/80.jpg	random	0	0	0	0.203677	K		2026-03-19T14:15:52
261	scripts/test photo for similarity_label_tool/149.jpg	__PCG_GENERATED__	pcg_generated	1	44395062	1	0.230174	K		2026-03-19T14:15:53
262	scripts/test photo for similarity_label_tool/170.jpg	scripts/test photo for similarity_label_tool/98.jpg	random	0	0	0	0.235215	K		2026-03-19T14:15:54
263	scripts/test photo for similarity_label_tool/31.jpg	scripts/test photo for similarity_label_tool/47.jpg	random	0	0	0	0.202659	K		2026-03-19T14:15:55
264	scripts/test photo for similarity_label_tool/113.jpg	__PCG_GENERATED__	pcg_generated	1	44422590	1	0.328484	K		2026-03-19T14:15:56
265	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	0	0.231636	K		2026-03-19T14:15:57
266	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	0	0.247831	K		2026-03-19T14:15:58
267	scripts/test photo for similarity_label_tool/77.jpg	__PCG_GENERATED__	pcg_generated	1	44450118	2	0.590029	K		2026-03-19T14:16:00
268	scripts/test photo for similarity_label_tool/128.jpg	scripts/test photo for similarity_label_tool/8.jpg	random	0	0	0	0.222732	K		2026-03-19T14:16:01
269	scripts/test photo for similarity_label_tool/131.jpg	scripts/test photo for similarity_label_tool/68.jpg	random	0	0	0	0.214056	K		2026-03-19T14:16:02
270	scripts/test photo for similarity_label_tool/14.jpg	__PCG_GENERATED__	pcg_generated	1	44477646	2	0.480699	K		2026-03-19T14:16:03
271	scripts/test photo for similarity_label_tool/170.jpg	scripts/test photo for similarity_label_tool/80.jpg	random	0	0	1	0.291965	K		2026-03-19T14:16:05
272	scripts/test photo for similarity_label_tool/104.jpg	scripts/test photo for similarity_label_tool/131.jpg	random	0	0	1	0.258229	K		2026-03-19T14:16:09
273	scripts/test photo for similarity_label_tool/8.jpg	__PCG_GENERATED__	pcg_generated	1	44505174	2	0.353248	K		2026-03-19T14:16:11
274	scripts/test photo for similarity_label_tool/47.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	0	0.200007	K		2026-03-19T14:16:12
275	scripts/test photo for similarity_label_tool/158.jpg	scripts/test photo for similarity_label_tool/65.jpg	random	0	0	0	0.177635	K		2026-03-19T14:16:13
276	scripts/test photo for similarity_label_tool/116.jpg	__PCG_GENERATED__	pcg_generated	1	44532702	2	0.391729	K		2026-03-19T14:16:18
277	scripts/test photo for similarity_label_tool/170.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	1	0.297142	K		2026-03-19T14:16:19
278	scripts/test photo for similarity_label_tool/34.jpg	scripts/test photo for similarity_label_tool/68.jpg	random	0	0	0	0.18087	K		2026-03-19T14:16:19
279	scripts/test photo for similarity_label_tool/167.jpg	__PCG_GENERATED__	pcg_generated	1	44560230	0	0.308371	K		2026-03-19T14:16:21
280	scripts/test photo for similarity_label_tool/47.jpg	scripts/test photo for similarity_label_tool/8.jpg	random	0	0	0	0.175567	K		2026-03-19T14:16:22
281	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/68.jpg	random	0	0	0	0.198542	K		2026-03-19T14:16:23
282	scripts/test photo for similarity_label_tool/146.jpg	__PCG_GENERATED__	pcg_generated	1	44587758	1	0.258396	K		2026-03-19T14:16:23
283	scripts/test photo for similarity_label_tool/128.jpg	scripts/test photo for similarity_label_tool/146.jpg	random	0	0	1	0.347724	K		2026-03-19T14:16:25
284	scripts/test photo for similarity_label_tool/38.jpg	scripts/test photo for similarity_label_tool/65.jpg	random	0	0	0	0.202308	K		2026-03-19T14:16:25
285	scripts/test photo for similarity_label_tool/179.jpg	__PCG_GENERATED__	pcg_generated	1	44615286	0	0.256037	K		2026-03-19T14:16:26
286	scripts/test photo for similarity_label_tool/116.jpg	scripts/test photo for similarity_label_tool/167.jpg	random	0	0	0	0.170768	K		2026-03-19T14:16:27
287	scripts/test photo for similarity_label_tool/182.jpg	scripts/test photo for similarity_label_tool/77.jpg	random	0	0	0	0.193844	K		2026-03-19T14:16:28
288	scripts/test photo for similarity_label_tool/32.jpg	__PCG_GENERATED__	pcg_generated	1	44642814	2	0.606982	K		2026-03-19T14:16:29
289	scripts/test photo for similarity_label_tool/134.jpg	scripts/test photo for similarity_label_tool/14.jpg	random	0	0	0	0.23949	K		2026-03-19T14:16:30
290	scripts/test photo for similarity_label_tool/71.jpg	scripts/test photo for similarity_label_tool/86.jpg	random	0	0	0	0.212203	K		2026-03-19T14:16:31
291	scripts/test photo for similarity_label_tool/74.jpg	__PCG_GENERATED__	pcg_generated	1	44670342	3	0.282505	K		2026-03-19T14:16:33
292	scripts/test photo for similarity_label_tool/161.jpg	scripts/test photo for similarity_label_tool/179.jpg	random	0	0	0	0.248207	K		2026-03-19T14:16:34
293	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/71.jpg	random	0	0	0	0.170526	K		2026-03-19T14:16:35
294	scripts/test photo for similarity_label_tool/164.jpg	__PCG_GENERATED__	pcg_generated	1	44697870	1	0.461669	K		2026-03-19T14:16:36
295	scripts/test photo for similarity_label_tool/65.jpg	scripts/test photo for similarity_label_tool/8.jpg	random	0	0	0	0.212324	K		2026-03-19T14:16:37
296	scripts/test photo for similarity_label_tool/104.jpg	scripts/test photo for similarity_label_tool/14.jpg	random	0	0	0	0.237445	K		2026-03-19T14:16:37
297	scripts/test photo for similarity_label_tool/128.jpg	__PCG_GENERATED__	pcg_generated	1	44725398	1	0.500961	K		2026-03-19T14:16:39
298	scripts/test photo for similarity_label_tool/134.jpg	scripts/test photo for similarity_label_tool/34.jpg	random	0	0	0	0.233008	K		2026-03-19T14:16:40
299	scripts/test photo for similarity_label_tool/158.jpg	scripts/test photo for similarity_label_tool/17.jpg	random	0	0	0	0.177311	K		2026-03-19T14:16:40
300	scripts/test photo for similarity_label_tool/164.jpg	__PCG_GENERATED__	pcg_generated	1	44752926	1	0.273013	K		2026-03-19T14:16:42
301	scripts/test photo for similarity_label_tool/146.jpg	scripts/test photo for similarity_label_tool/8.jpg	random	0	0	0	0.251143	K		2026-03-19T14:16:42
302	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/95.jpg	random	0	0	1	0.261194	K		2026-03-19T14:16:43
303	scripts/test photo for similarity_label_tool/161.jpg	__PCG_GENERATED__	pcg_generated	1	44780454	1	0.246621	K		2026-03-19T14:16:44
304	scripts/test photo for similarity_label_tool/146.jpg	scripts/test photo for similarity_label_tool/56.jpg	random	0	0	0	0.206167	K		2026-03-19T14:16:45
305	scripts/test photo for similarity_label_tool/161.jpg	scripts/test photo for similarity_label_tool/33.jpg	random	0	0	0	0.16549	K		2026-03-19T14:16:45
306	scripts/test photo for similarity_label_tool/137.jpg	__PCG_GENERATED__	pcg_generated	1	44807982	1	0.241261	K		2026-03-19T14:16:47
307	scripts/test photo for similarity_label_tool/17.jpg	scripts/test photo for similarity_label_tool/20.jpg	random	0	0	2	0.843718	K		2026-03-19T14:16:48
308	scripts/test photo for similarity_label_tool/35.jpg	scripts/test photo for similarity_label_tool/98.jpg	random	0	0	0	0.207747	K		2026-03-19T14:16:49
309	scripts/test photo for similarity_label_tool/34.jpg	__PCG_GENERATED__	pcg_generated	1	44835510	2	0.501651	K		2026-03-19T14:16:50
310	scripts/test photo for similarity_label_tool/26.jpg	scripts/test photo for similarity_label_tool/74.jpg	random	0	0	0	0.178485	K		2026-03-19T14:16:51
311	scripts/test photo for similarity_label_tool/158.jpg	scripts/test photo for similarity_label_tool/92.jpg	random	0	0	0	0.235315	K		2026-03-19T14:16:52
312	scripts/test photo for similarity_label_tool/146.jpg	__PCG_GENERATED__	pcg_generated	1	44863038	0	0.334057	K		2026-03-19T14:16:57
313	scripts/test photo for similarity_label_tool/80.jpg	scripts/test photo for similarity_label_tool/98.jpg	random	0	0	0	0.135332	K		2026-03-19T14:16:59
314	scripts/test photo for similarity_label_tool/131.jpg	scripts/test photo for similarity_label_tool/143.jpg	random	0	0	1	0.3219	K		2026-03-19T14:17:02
315	scripts/test photo for similarity_label_tool/38.jpg	__PCG_GENERATED__	pcg_generated	1	44890566	3	0.600842	K		2026-03-19T14:17:03
316	scripts/test photo for similarity_label_tool/29.jpg	scripts/test photo for similarity_label_tool/95.jpg	random	0	0	0	0.206157	K		2026-03-19T14:17:04
317	scripts/test photo for similarity_label_tool/143.jpg	scripts/test photo for similarity_label_tool/98.jpg	random	0	0	0	0.230993	K		2026-03-19T14:17:05
318	scripts/test photo for similarity_label_tool/89.jpg	__PCG_GENERATED__	pcg_generated	1	44918094	2	0.456184	K		2026-03-19T14:17:06
319	scripts/test photo for similarity_label_tool/107.jpg	scripts/test photo for similarity_label_tool/116.jpg	random	0	0	0	0.235745	K		2026-03-19T14:17:07
320	scripts/test photo for similarity_label_tool/173.jpg	scripts/test photo for similarity_label_tool/30.jpg	random	0	0	0	0.244482	K		2026-03-19T14:17:08
321	scripts/test photo for similarity_label_tool/35.jpg	__PCG_GENERATED__	pcg_generated	1	44945622	1	0.326092	K		2026-03-19T14:17:09
322	scripts/test photo for similarity_label_tool/161.jpg	scripts/test photo for similarity_label_tool/44.jpg	random	0	0	0	0.237029	K		2026-03-19T14:17:10
323	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/65.jpg	random	0	0	0	0.176873	K		2026-03-19T14:17:10
324	scripts/test photo for similarity_label_tool/33.jpg	__PCG_GENERATED__	pcg_generated	1	44973150	1	0.552811	K		2026-03-19T14:17:11
325	scripts/test photo for similarity_label_tool/119.jpg	scripts/test photo for similarity_label_tool/167.jpg	random	0	0	0	0.199342	K		2026-03-19T14:17:12
326	scripts/test photo for similarity_label_tool/28.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.163701	K		2026-03-19T14:17:13
327	scripts/test photo for similarity_label_tool/110.jpg	__PCG_GENERATED__	pcg_generated	1	45000678	1	0.328952	K		2026-03-19T14:17:14
328	scripts/test photo for similarity_label_tool/134.jpg	scripts/test photo for similarity_label_tool/143.jpg	random	0	0	1	0.320848	K		2026-03-19T14:17:15
329	scripts/test photo for similarity_label_tool/107.jpg	scripts/test photo for similarity_label_tool/41.jpg	random	0	0	0	0.231025	K		2026-03-19T14:17:16
330	scripts/test photo for similarity_label_tool/30.jpg	__PCG_GENERATED__	pcg_generated	1	45028206	1	0.264861	K		2026-03-19T14:17:19
331	scripts/test photo for similarity_label_tool/101.jpg	scripts/test photo for similarity_label_tool/173.jpg	random	0	0	2	0.357079	K		2026-03-19T14:17:20
332	scripts/test photo for similarity_label_tool/23.jpg	scripts/test photo for similarity_label_tool/89.jpg	random	0	0	0	0.204908	K		2026-03-19T14:17:21
333	scripts/test photo for similarity_label_tool/32.jpg	__PCG_GENERATED__	pcg_generated	1	45055734	2	0.579741	K		2026-03-19T14:17:22
334	scripts/test photo for similarity_label_tool/26.jpg	scripts/test photo for similarity_label_tool/68.jpg	random	0	0	0	0.168977	K		2026-03-19T14:17:23
335	scripts/test photo for similarity_label_tool/47.jpg	scripts/test photo for similarity_label_tool/92.jpg	random	0	0	0	0.219688	K		2026-03-19T14:17:23
336	scripts/test photo for similarity_label_tool/128.jpg	__PCG_GENERATED__	pcg_generated	1	45083262	2	0.370492	K		2026-03-19T14:17:25
337	scripts/test photo for similarity_label_tool/34.jpg	scripts/test photo for similarity_label_tool/47.jpg	random	0	0	0	0.219159	K		2026-03-19T14:17:26
338	scripts/test photo for similarity_label_tool/134.jpg	scripts/test photo for similarity_label_tool/164.jpg	random	0	0	1	0.279284	K		2026-03-19T14:17:27
339	scripts/test photo for similarity_label_tool/26.jpg	__PCG_GENERATED__	pcg_generated	1	45110790	2	0.324005	K		2026-03-19T14:17:29
340	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/173.jpg	random	0	0	2	0.515586	K		2026-03-19T14:17:30
341	scripts/test photo for similarity_label_tool/34.jpg	scripts/test photo for similarity_label_tool/92.jpg	random	0	0	0	0.161162	K		2026-03-19T14:17:31
342	scripts/test photo for similarity_label_tool/44.jpg	__PCG_GENERATED__	pcg_generated	1	45138318	0	0.267649	K		2026-03-19T14:17:32
343	scripts/test photo for similarity_label_tool/158.jpg	scripts/test photo for similarity_label_tool/86.jpg	random	0	0	0	0.187247	K		2026-03-19T14:17:33
344	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/31.jpg	random	0	0	0	0.174166	K		2026-03-19T14:17:34
345	scripts/test photo for similarity_label_tool/140.jpg	__PCG_GENERATED__	pcg_generated	1	45165846	0	0.252496	K		2026-03-19T14:17:35
346	scripts/test photo for similarity_label_tool/34.jpg	scripts/test photo for similarity_label_tool/77.jpg	random	0	0	0	0.18248	K		2026-03-19T14:17:35
347	scripts/test photo for similarity_label_tool/119.jpg	scripts/test photo for similarity_label_tool/44.jpg	random	0	0	0	0.219771	K		2026-03-19T14:17:36
348	scripts/test photo for similarity_label_tool/128.jpg	__PCG_GENERATED__	pcg_generated	1	45193374	0	0.238407	K		2026-03-19T14:17:37
349	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.183617	K		2026-03-19T14:17:38
350	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/20.jpg	random	0	0	0	0.165798	K		2026-03-19T14:17:38
351	scripts/test photo for similarity_label_tool/179.jpg	__PCG_GENERATED__	pcg_generated	1	45220902	3	0.633424	K		2026-03-19T14:17:41
352	scripts/test photo for similarity_label_tool/170.jpg	scripts/test photo for similarity_label_tool/34.jpg	random	0	0	0	0.181509	K		2026-03-19T14:17:41
353	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/17.jpg	random	0	0	0	0.176543	K		2026-03-19T14:17:42
354	scripts/test photo for similarity_label_tool/167.jpg	__PCG_GENERATED__	pcg_generated	1	45248430	1	0.365766	K		2026-03-19T14:17:44
355	scripts/test photo for similarity_label_tool/149.jpg	scripts/test photo for similarity_label_tool/38.jpg	random	0	0	0	0.159143	K		2026-03-19T14:17:44
356	scripts/test photo for similarity_label_tool/122.jpg	scripts/test photo for similarity_label_tool/27.jpg	random	0	0	0	0.214445	K		2026-03-19T14:17:45
357	scripts/test photo for similarity_label_tool/146.jpg	__PCG_GENERATED__	pcg_generated	1	45275958	1	0.331244	K		2026-03-19T14:17:46
358	scripts/test photo for similarity_label_tool/134.jpg	scripts/test photo for similarity_label_tool/170.jpg	random	0	0	0	0.272001	K		2026-03-19T14:17:46
359	scripts/test photo for similarity_label_tool/167.jpg	scripts/test photo for similarity_label_tool/35.jpg	random	0	0	0	0.224138	K		2026-03-19T14:17:47
360	scripts/test photo for similarity_label_tool/89.jpg	__PCG_GENERATED__	pcg_generated	1	45303486	1	0.250214	K		2026-03-19T14:17:48
361	scripts/test photo for similarity_label_tool/47.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.197284	K		2026-03-19T14:17:48
362	scripts/test photo for similarity_label_tool/131.jpg	scripts/test photo for similarity_label_tool/31.jpg	random	0	0	0	0.22235	K		2026-03-19T14:17:49
363	scripts/test photo for similarity_label_tool/32.jpg	__PCG_GENERATED__	pcg_generated	1	45331014	1	0.484923	K		2026-03-19T14:17:51
364	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/28.jpg	random	0	0	0	0.201472	K		2026-03-19T14:17:52
365	scripts/test photo for similarity_label_tool/17.jpg	scripts/test photo for similarity_label_tool/27.jpg	random	0	0	0	0.139631	K		2026-03-19T14:17:52
366	scripts/test photo for similarity_label_tool/38.jpg	__PCG_GENERATED__	pcg_generated	1	45358542	1	0.268615	K		2026-03-19T14:17:54
367	scripts/test photo for similarity_label_tool/101.jpg	scripts/test photo for similarity_label_tool/74.jpg	random	0	0	0	0.199203	K		2026-03-19T14:17:54
368	scripts/test photo for similarity_label_tool/149.jpg	scripts/test photo for similarity_label_tool/152.jpg	random	0	0	3	0.784813	K		2026-03-19T14:17:57
369	scripts/test photo for similarity_label_tool/27.jpg	__PCG_GENERATED__	pcg_generated	1	45386070	1	0.460747	K		2026-03-19T14:17:58
370	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/173.jpg	random	0	0	1	0.25509	K		2026-03-19T14:18:34
371	scripts/test photo for similarity_label_tool/29.jpg	scripts/test photo for similarity_label_tool/65.jpg	random	0	0	0	0.22239	K		2026-03-19T14:18:34
372	scripts/test photo for similarity_label_tool/14.jpg	__PCG_GENERATED__	pcg_generated	1	45413598	2	0.455514	K		2026-03-19T14:18:37
373	scripts/test photo for similarity_label_tool/30.jpg	scripts/test photo for similarity_label_tool/33.jpg	random	0	0	0	0.140992	K		2026-03-19T14:18:37
374	scripts/test photo for similarity_label_tool/176.jpg	scripts/test photo for similarity_label_tool/35.jpg	random	0	0	0	0.213391	K		2026-03-19T14:18:38
375	scripts/test photo for similarity_label_tool/35.jpg	__PCG_GENERATED__	pcg_generated	1	45441126	2	0.462204	K		2026-03-19T14:18:39
376	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/20.jpg	random	0	0	0	0.228434	K		2026-03-19T14:18:40
377	scripts/test photo for similarity_label_tool/182.jpg	scripts/test photo for similarity_label_tool/65.jpg	random	0	0	0	0.210919	K		2026-03-19T14:18:40
378	scripts/test photo for similarity_label_tool/155.jpg	__PCG_GENERATED__	pcg_generated	1	45468654	3	0.500042	K		2026-03-19T14:18:42
379	scripts/test photo for similarity_label_tool/83.jpg	scripts/test photo for similarity_label_tool/95.jpg	random	0	0	0	0.149875	K		2026-03-19T14:18:42
380	scripts/test photo for similarity_label_tool/47.jpg	scripts/test photo for similarity_label_tool/65.jpg	random	0	0	0	0.187924	K		2026-03-19T14:18:43
381	scripts/test photo for similarity_label_tool/74.jpg	__PCG_GENERATED__	pcg_generated	1	45496182	2	0.384674	K		2026-03-19T14:18:44
382	scripts/test photo for similarity_label_tool/128.jpg	scripts/test photo for similarity_label_tool/34.jpg	random	0	0	0	0.234744	K		2026-03-19T14:18:45
383	scripts/test photo for similarity_label_tool/113.jpg	scripts/test photo for similarity_label_tool/149.jpg	random	0	0	0	0.191375	K		2026-03-19T14:18:46
384	scripts/test photo for similarity_label_tool/56.jpg	__PCG_GENERATED__	pcg_generated	1	45523710	0	0.281531	K		2026-03-19T14:18:48
385	scripts/test photo for similarity_label_tool/20.jpg	scripts/test photo for similarity_label_tool/34.jpg	random	0	0	0	0.247793	K		2026-03-19T14:18:49
386	scripts/test photo for similarity_label_tool/31.jpg	scripts/test photo for similarity_label_tool/32.jpg	random	0	0	0	0.241627	K		2026-03-19T14:18:49
387	scripts/test photo for similarity_label_tool/56.jpg	__PCG_GENERATED__	pcg_generated	1	45551238	0	0.261107	K		2026-03-19T14:18:50
388	scripts/test photo for similarity_label_tool/113.jpg	scripts/test photo for similarity_label_tool/158.jpg	random	0	0	0	0.195644	K		2026-03-19T14:18:51
389	scripts/test photo for similarity_label_tool/71.jpg	scripts/test photo for similarity_label_tool/92.jpg	random	0	0	0	0.198715	K		2026-03-19T14:18:51
390	scripts/test photo for similarity_label_tool/11.jpg	__PCG_GENERATED__	pcg_generated	1	45578766	2	0.325985	K		2026-03-19T14:18:52
391	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/50.jpg	random	0	0	0	0.287708	K		2026-03-19T14:18:53
392	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/35.jpg	random	0	0	0	0.133259	K		2026-03-19T14:18:54
393	scripts/test photo for similarity_label_tool/14.jpg	__PCG_GENERATED__	pcg_generated	1	45606294	2	0.334624	K		2026-03-19T14:19:20
394	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/68.jpg	random	0	0	0	0.218693	K		2026-03-19T14:19:21
395	scripts/test photo for similarity_label_tool/104.jpg	scripts/test photo for similarity_label_tool/107.jpg	random	0	0	2	0.520649	K		2026-03-19T14:19:23
396	scripts/test photo for similarity_label_tool/71.jpg	__PCG_GENERATED__	pcg_generated	1	45633822	2	0.515156	K		2026-03-19T14:19:24
397	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/98.jpg	random	0	0	0	0.240444	K		2026-03-19T14:19:24
398	scripts/test photo for similarity_label_tool/182.jpg	scripts/test photo for similarity_label_tool/31.jpg	random	0	0	0	0.217645	K		2026-03-19T14:19:25
399	scripts/test photo for similarity_label_tool/107.jpg	__PCG_GENERATED__	pcg_generated	1	45661350	2	0.311261	K		2026-03-19T14:19:28
400	scripts/test photo for similarity_label_tool/56.jpg	scripts/test photo for similarity_label_tool/77.jpg	random	0	0	0	0.192911	K		2026-03-19T14:24:55
401	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/179.jpg	random	0	0	0	0.252042	K		2026-03-19T14:24:56
402	scripts/test photo for similarity_label_tool/68.jpg	__PCG_GENERATED__	pcg_generated	1	45688878	2	0.34556	K		2026-03-19T14:24:58
403	scripts/test photo for similarity_label_tool/28.jpg	scripts/test photo for similarity_label_tool/32.jpg	random	0	0	0	0.183474	K		2026-03-19T14:24:58
404	scripts/test photo for similarity_label_tool/134.jpg	scripts/test photo for similarity_label_tool/41.jpg	random	0	0	0	0.217033	K		2026-03-19T14:24:59
405	scripts/test photo for similarity_label_tool/155.jpg	__PCG_GENERATED__	pcg_generated	1	45716406	1	0.354963	K		2026-03-19T14:25:00
406	scripts/test photo for similarity_label_tool/167.jpg	scripts/test photo for similarity_label_tool/38.jpg	random	0	0	1	0.250809	K		2026-03-19T14:25:01
407	scripts/test photo for similarity_label_tool/17.jpg	scripts/test photo for similarity_label_tool/185.jpg	random	0	0	0	0.176632	K		2026-03-19T14:25:02
408	scripts/test photo for similarity_label_tool/17.jpg	__PCG_GENERATED__	pcg_generated	1	45743934	0	0.465062	K		2026-03-19T14:25:04
409	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/140.jpg	random	0	0	1	0.394017	K		2026-03-19T14:25:05
410	scripts/test photo for similarity_label_tool/33.jpg	scripts/test photo for similarity_label_tool/38.jpg	random	0	0	0	0.198879	K		2026-03-19T14:25:06
411	scripts/test photo for similarity_label_tool/146.jpg	__PCG_GENERATED__	pcg_generated	1	45771462	0	0.246657	K		2026-03-19T14:25:07
412	scripts/test photo for similarity_label_tool/101.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.143665	K		2026-03-19T14:25:08
413	scripts/test photo for similarity_label_tool/50.jpg	scripts/test photo for similarity_label_tool/8.jpg	random	0	0	0	0.18043	K		2026-03-19T14:25:09
414	scripts/test photo for similarity_label_tool/110.jpg	__PCG_GENERATED__	pcg_generated	1	45798990	2	0.409968	K		2026-03-19T14:25:12
415	scripts/test photo for similarity_label_tool/56.jpg	scripts/test photo for similarity_label_tool/80.jpg	random	0	0	1	0.263429	K		2026-03-19T14:25:13
416	scripts/test photo for similarity_label_tool/116.jpg	scripts/test photo for similarity_label_tool/56.jpg	random	0	0	0	0.192384	K		2026-03-19T14:25:13
417	scripts/test photo for similarity_label_tool/137.jpg	__PCG_GENERATED__	pcg_generated	1	45826518	1	0.418171	K		2026-03-19T14:25:14
418	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/173.jpg	random	0	0	0	0.234174	K		2026-03-19T14:25:15
419	scripts/test photo for similarity_label_tool/38.jpg	scripts/test photo for similarity_label_tool/95.jpg	random	0	0	0	0.211506	K		2026-03-19T14:25:16
420	scripts/test photo for similarity_label_tool/86.jpg	__PCG_GENERATED__	pcg_generated	1	45854046	2	0.367596	K		2026-03-19T14:25:17
421	scripts/test photo for similarity_label_tool/179.jpg	scripts/test photo for similarity_label_tool/23.jpg	random	0	0	0	0.201587	K		2026-03-19T14:25:18
422	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/27.jpg	random	0	0	0	0.22255	K		2026-03-19T14:25:18
423	scripts/test photo for similarity_label_tool/92.jpg	__PCG_GENERATED__	pcg_generated	1	45881574	2	0.541113	K		2026-03-19T14:25:23
424	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/86.jpg	random	0	0	0	0.247905	K		2026-03-19T14:25:24
425	scripts/test photo for similarity_label_tool/119.jpg	scripts/test photo for similarity_label_tool/77.jpg	random	0	0	0	0.187506	K		2026-03-19T14:25:24
426	scripts/test photo for similarity_label_tool/28.jpg	__PCG_GENERATED__	pcg_generated	1	45909102	3	0.373322	K		2026-03-19T14:25:27
427	scripts/test photo for similarity_label_tool/122.jpg	scripts/test photo for similarity_label_tool/179.jpg	random	0	0	0	0.180064	K		2026-03-19T14:25:27
428	scripts/test photo for similarity_label_tool/179.jpg	scripts/test photo for similarity_label_tool/68.jpg	random	0	0	0	0.202184	K		2026-03-19T14:25:28
429	scripts/test photo for similarity_label_tool/80.jpg	__PCG_GENERATED__	pcg_generated	1	45936630	1	0.277302	K		2026-03-19T14:25:29
430	scripts/test photo for similarity_label_tool/23.jpg	scripts/test photo for similarity_label_tool/34.jpg	random	0	0	0	0.240081	K		2026-03-19T14:25:30
431	scripts/test photo for similarity_label_tool/27.jpg	scripts/test photo for similarity_label_tool/30.jpg	random	0	0	0	0.211743	K		2026-03-19T14:25:30
432	scripts/test photo for similarity_label_tool/41.jpg	__PCG_GENERATED__	pcg_generated	1	45964158	1	0.298332	K		2026-03-19T14:25:59
433	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/92.jpg	random	0	0	0	0.231753	K		2026-03-19T14:26:00
434	scripts/test photo for similarity_label_tool/50.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.205724	K		2026-03-19T14:26:00
435	scripts/test photo for similarity_label_tool/155.jpg	__PCG_GENERATED__	pcg_generated	1	45991686	2	0.414404	K		2026-03-19T14:26:02
436	scripts/test photo for similarity_label_tool/176.jpg	scripts/test photo for similarity_label_tool/31.jpg	random	0	0	0	0.198152	K		2026-03-19T14:26:03
437	scripts/test photo for similarity_label_tool/44.jpg	scripts/test photo for similarity_label_tool/71.jpg	random	0	0	0	0.176387	K		2026-03-19T14:26:04
438	scripts/test photo for similarity_label_tool/137.jpg	__PCG_GENERATED__	pcg_generated	1	46019214	2	0.357139	K		2026-03-19T14:26:06
439	scripts/test photo for similarity_label_tool/20.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.246472	K		2026-03-19T14:26:07
440	scripts/test photo for similarity_label_tool/27.jpg	scripts/test photo for similarity_label_tool/86.jpg	random	0	0	0	0.219634	K		2026-03-19T14:26:08
441	scripts/test photo for similarity_label_tool/33.jpg	__PCG_GENERATED__	pcg_generated	1	46046742	2	0.386893	K		2026-03-19T14:26:09
442	scripts/test photo for similarity_label_tool/128.jpg	scripts/test photo for similarity_label_tool/47.jpg	random	0	0	0	0.230938	K		2026-03-19T14:26:10
443	scripts/test photo for similarity_label_tool/182.jpg	scripts/test photo for similarity_label_tool/8.jpg	random	0	0	0	0.212935	K		2026-03-19T14:26:11
444	scripts/test photo for similarity_label_tool/185.jpg	__PCG_GENERATED__	pcg_generated	1	46074270	2	0.404773	K		2026-03-19T14:26:14
445	scripts/test photo for similarity_label_tool/143.jpg	scripts/test photo for similarity_label_tool/176.jpg	random	0	0	1	0.360904	K		2026-03-19T14:26:15
446	scripts/test photo for similarity_label_tool/23.jpg	scripts/test photo for similarity_label_tool/56.jpg	random	0	0	0	0.180339	K		2026-03-19T14:26:15
447	scripts/test photo for similarity_label_tool/17.jpg	__PCG_GENERATED__	pcg_generated	1	46101798	2	0.521786	K		2026-03-19T14:26:17
448	scripts/test photo for similarity_label_tool/185.jpg	scripts/test photo for similarity_label_tool/32.jpg	random	0	0	0	0.174246	K		2026-03-19T14:26:17
449	scripts/test photo for similarity_label_tool/140.jpg	scripts/test photo for similarity_label_tool/146.jpg	random	0	0	2	0.429829	K		2026-03-19T14:26:20
450	scripts/test photo for similarity_label_tool/80.jpg	__PCG_GENERATED__	pcg_generated	1	46129326	0	0.284062	K		2026-03-19T14:26:21
451	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/176.jpg	random	0	0	0	0.253412	K		2026-03-19T14:26:22
452	scripts/test photo for similarity_label_tool/149.jpg	scripts/test photo for similarity_label_tool/41.jpg	random	0	0	2	0.345898	K		2026-03-19T14:26:24
453	scripts/test photo for similarity_label_tool/86.jpg	__PCG_GENERATED__	pcg_generated	1	46156854	0	0.272842	K		2026-03-19T14:26:25
454	scripts/test photo for similarity_label_tool/155.jpg	scripts/test photo for similarity_label_tool/158.jpg	random	0	0	2	0.598257	K		2026-03-19T14:26:27
455	scripts/test photo for similarity_label_tool/26.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.236217	K		2026-03-19T14:26:28
456	scripts/test photo for similarity_label_tool/33.jpg	__PCG_GENERATED__	pcg_generated	1	46184382	2	0.607034	K		2026-03-19T14:26:29
457	scripts/test photo for similarity_label_tool/113.jpg	scripts/test photo for similarity_label_tool/122.jpg	random	0	0	2	0.490176	K		2026-03-19T14:26:30
458	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/14.jpg	random	0	0	0	0.24078	K		2026-03-19T14:26:31
459	scripts/test photo for similarity_label_tool/179.jpg	__PCG_GENERATED__	pcg_generated	1	46211910	1	0.44842	K		2026-03-19T14:26:36
460	scripts/test photo for similarity_label_tool/125.jpg	scripts/test photo for similarity_label_tool/41.jpg	random	0	0	0	0.227861	K		2026-03-19T14:26:36
461	scripts/test photo for similarity_label_tool/110.jpg	scripts/test photo for similarity_label_tool/137.jpg	random	0	0	1	0.287343	K		2026-03-19T14:26:38
462	scripts/test photo for similarity_label_tool/125.jpg	__PCG_GENERATED__	pcg_generated	1	46239438	3	0.360515	K		2026-03-19T14:26:39
463	scripts/test photo for similarity_label_tool/158.jpg	scripts/test photo for similarity_label_tool/170.jpg	random	0	0	0	0.205622	K		2026-03-19T14:26:40
464	scripts/test photo for similarity_label_tool/179.jpg	scripts/test photo for similarity_label_tool/26.jpg	random	0	0	0	0.200463	K		2026-03-19T14:26:41
465	scripts/test photo for similarity_label_tool/143.jpg	__PCG_GENERATED__	pcg_generated	1	46266966	1	0.343542	K		2026-03-19T14:26:42
466	scripts/test photo for similarity_label_tool/11.jpg	scripts/test photo for similarity_label_tool/170.jpg	random	0	0	0	0.214606	K		2026-03-19T14:26:42
467	scripts/test photo for similarity_label_tool/137.jpg	scripts/test photo for similarity_label_tool/74.jpg	random	0	0	0	0.178928	K		2026-03-19T14:26:43
468	scripts/test photo for similarity_label_tool/122.jpg	__PCG_GENERATED__	pcg_generated	1	46294494	2	0.298737	K		2026-03-19T14:26:44
469	scripts/test photo for similarity_label_tool/167.jpg	scripts/test photo for similarity_label_tool/170.jpg	random	0	0	2	0.514186	K		2026-03-19T14:26:46
470	scripts/test photo for similarity_label_tool/56.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	1	0.257505	K		2026-03-19T14:26:47
471	scripts/test photo for similarity_label_tool/140.jpg	__PCG_GENERATED__	pcg_generated	1	46322022	0	0.281176	K		2026-03-19T14:26:48
472	scripts/test photo for similarity_label_tool/29.jpg	scripts/test photo for similarity_label_tool/92.jpg	random	0	0	0	0.203145	K		2026-03-19T14:26:49
473	scripts/test photo for similarity_label_tool/104.jpg	scripts/test photo for similarity_label_tool/38.jpg	random	0	0	0	0.178758	K		2026-03-19T14:26:50
474	scripts/test photo for similarity_label_tool/47.jpg	__PCG_GENERATED__	pcg_generated	1	46349550	2	0.35354	K		2026-03-19T14:26:52
475	scripts/test photo for similarity_label_tool/77.jpg	scripts/test photo for similarity_label_tool/80.jpg	random	0	0	0	0.209947	K		2026-03-19T14:26:52
476	scripts/test photo for similarity_label_tool/28.jpg	scripts/test photo for similarity_label_tool/50.jpg	random	0	0	0	0.218024	K		2026-03-19T14:26:53
477	scripts/test photo for similarity_label_tool/27.jpg	__PCG_GENERATED__	pcg_generated	1	46377078	1	0.314702	K		2026-03-19T14:26:54
478	scripts/test photo for similarity_label_tool/167.jpg	scripts/test photo for similarity_label_tool/182.jpg	random	0	0	0	0.217006	K		2026-03-19T14:26:54
479	scripts/test photo for similarity_label_tool/101.jpg	scripts/test photo for similarity_label_tool/92.jpg	random	0	0	2	0.515442	K		2026-03-19T14:26:57
480	scripts/test photo for similarity_label_tool/26.jpg	__PCG_GENERATED__	pcg_generated	1	46404606	3	0.765491	K		2026-03-19T14:26:59
481	scripts/test photo for similarity_label_tool/152.jpg	scripts/test photo for similarity_label_tool/161.jpg	random	0	0	0	0.207203	K		2026-03-19T14:27:00
482	scripts/test photo for similarity_label_tool/167.jpg	scripts/test photo for similarity_label_tool/50.jpg	random	0	0	0	0.175971	K		2026-03-19T14:27:01
483	scripts/test photo for similarity_label_tool/143.jpg	__PCG_GENERATED__	pcg_generated	1	46432134	1	0.445632	K		2026-03-19T14:27:03
484	scripts/test photo for similarity_label_tool/77.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.216448	K		2026-03-19T14:27:03
485	scripts/test photo for similarity_label_tool/74.jpg	scripts/test photo for similarity_label_tool/95.jpg	random	0	0	0	0.201949	K		2026-03-19T14:27:04
486	scripts/test photo for similarity_label_tool/47.jpg	__PCG_GENERATED__	pcg_generated	1	46459662	1	0.476974	K		2026-03-19T14:27:05
487	scripts/test photo for similarity_label_tool/170.jpg	scripts/test photo for similarity_label_tool/26.jpg	random	0	0	0	0.220126	K		2026-03-19T14:27:07
488	scripts/test photo for similarity_label_tool/26.jpg	scripts/test photo for similarity_label_tool/47.jpg	random	0	0	0	0.194296	K		2026-03-19T14:27:08
489	scripts/test photo for similarity_label_tool/29.jpg	__PCG_GENERATED__	pcg_generated	1	46487190	1	0.581309	K		2026-03-19T14:27:09
490	scripts/test photo for similarity_label_tool/30.jpg	scripts/test photo for similarity_label_tool/68.jpg	random	0	0	0	0.228669	K		2026-03-19T14:27:09
491	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/83.jpg	random	0	0	0	0.210812	K		2026-03-19T14:27:10
492	scripts/test photo for similarity_label_tool/173.jpg	__PCG_GENERATED__	pcg_generated	1	46514718	1	0.367031	K		2026-03-19T14:27:11
493	scripts/test photo for similarity_label_tool/14.jpg	scripts/test photo for similarity_label_tool/185.jpg	random	0	0	0	0.273473	K		2026-03-19T14:27:11
494	scripts/test photo for similarity_label_tool/146.jpg	scripts/test photo for similarity_label_tool/173.jpg	random	0	0	1	0.277868	K		2026-03-19T14:27:12
495	scripts/test photo for similarity_label_tool/83.jpg	__PCG_GENERATED__	pcg_generated	1	46542246	1	0.282008	K		2026-03-19T14:27:13
496	scripts/test photo for similarity_label_tool/104.jpg	scripts/test photo for similarity_label_tool/185.jpg	random	0	0	0	0.180052	K		2026-03-19T14:27:14
497	scripts/test photo for similarity_label_tool/158.jpg	scripts/test photo for similarity_label_tool/167.jpg	random	0	0	0	0.182773	K		2026-03-19T14:27:15
498	scripts/test photo for similarity_label_tool/29.jpg	__PCG_GENERATED__	pcg_generated	1	46569774	1	0.253331	K		2026-03-19T14:27:15
499	scripts/test photo for similarity_label_tool/34.jpg	scripts/test photo for similarity_label_tool/35.jpg	random	0	0	0	0.202099	K		2026-03-19T14:27:16
500	scripts/test photo for similarity_label_tool/17.jpg	scripts/test photo for similarity_label_tool/68.jpg	random	0	0	0	0.198299	K		2026-03-19T14:27:17"""

df = pd.read_csv(io.StringIO(data_str), sep='\t')

# Ensure similarity_score is float
df['similarity_score'] = pd.to_numeric(df['similarity_score'], errors='coerce')
# Drop NaN values if any
df = df.dropna(subset=['similarity_score'])

# Create a boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='label', y='similarity_score', data=df, palette='Set2')
sns.stripplot(x='label', y='similarity_score', data=df, color='black', alpha=0.3, jitter=True)

plt.title('Similarity Score Distribution by Label')
plt.xlabel('Label (0: Different, 3: Very Similar)')
plt.ylabel('Similarity Score')

# Save plot
plt.savefig('similarity_distribution_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved to similarity_distribution_plot.png")
