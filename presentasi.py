import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Netflix Originals Dashboard", page_icon=":clapper:", layout="wide")

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="NetflixOriginals.xlsx",
        engine="openpyxl",
        sheet_name="NetflixOriginals",
        usecols="A:F",  # Columns A to F are relevant
    )
    return df

# Tambahkan logo Netflix di bagian atas halaman
st.image("netflix.png", width=200)
st.title("Data Frame tanpa Filter ")

df = get_data_from_excel()
st.dataframe(df)

# --- SIDE BAR ------
st.sidebar.header("Please Filter Here:")
genre = st.sidebar.multiselect(
    "Select the Genre:",
    options=df["Genre"].unique(),
    default=df["Genre"].unique()
)

language = st.sidebar.multiselect(
    "Select the Language:",
    options=df["Language"].unique(),
    default=df["Language"].unique()
)

df_selection = df.query(
    "Genre == @genre and Language == @language"
)

st.title("Data Frame dengan Filter ")
st.dataframe(df_selection)

# --- MAINPAGE ---
st.title(":clapper: Netflix Originals Dashboard")
st.markdown("##")

# menampilkan skor rata-rata IMDB
average_score = round(df_selection["IMDB Score"].mean(), 1)
star_rating = ":star:" * int(round(average_score, 0))

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Average IMDB Score")
    st.subheader(f"{average_score} {star_rating}")

st.markdown("""---""")

# Visualisasi rata-rata Durasi berdasarkan genre
runtime_by_genre = (
    df_selection.groupby(by=["Genre"])[["Runtime"]].mean().sort_values(by="Runtime")
)

fig_genre_runtime = px.bar(
    runtime_by_genre,
    x="Runtime",
    y=runtime_by_genre.index,
    orientation="h",
    title="Average Runtime by Genre",
    color_discrete_sequence=["#0083B8"],
    template="plotly_white",
)

fig_genre_runtime.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="Average Runtime (minutes)"),
    yaxis=dict(title="Genre"),
)

st.plotly_chart(fig_genre_runtime, use_container_width=True)

# Visualisasi jumlah film berdasarkan bahasa
count_by_language = df_selection["Language"].value_counts().reset_index()
count_by_language.columns = ["Language", "Count"]

fig_language_count = px.pie(
    count_by_language,
    values="Count",
    names="Language",
    title="Number of Originals by Language",
    width=600
)

st.plotly_chart(fig_language_count)


# visualisasi rata rata skor IMDB berdasarkan genre
score_by_genre = df_selection.groupby("Genre")["IMDB Score"].mean().reset_index()

fig_genre_score = px.bar(
    score_by_genre,
    x="Genre",
    y="IMDB Score",
    title="Average IMDB Score by Genre",
    color_discrete_sequence=["#FF6347"],
    template="plotly_white",
)

fig_genre_score.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="Genre"),
    yaxis=dict(title="Average IMDB Score"),
)

st.plotly_chart(fig_genre_score, use_container_width=True)

# visualisasi rata-rata durasi berdasarkan bahasa
runtime_by_language = df_selection.groupby("Language")["Runtime"].mean().reset_index()

fig_language_runtime = px.line(
    runtime_by_language,
    x="Language",
    y="Runtime",
    title="Average Runtime by Language",
    markers=True,
    template="plotly_white",
)

fig_language_runtime.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="Language"),
    yaxis=dict(title="Average Runtime (minutes)"),
)

st.plotly_chart(fig_language_runtime, use_container_width=True)

# 3. Distribusi Skor IMDB
fig_imdb_distribution = px.histogram(
    df_selection,
    x="IMDB Score",
    nbins=20,
    title="Distribution of IMDB Scores",
    template="plotly_white",
    color_discrete_sequence=["#636EFA"]
)

fig_imdb_distribution.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="IMDB Score"),
    yaxis=dict(title="Count"),
)

st.plotly_chart(fig_imdb_distribution, use_container_width=True)

# 4. Top 10 Bahasa berdasarkan jumlah film 
top_languages = df_selection["Language"].value_counts().nlargest(10).reset_index()
top_languages.columns = ["Language", "Count"]

fig_top_languages = px.bar(
    top_languages,
    x="Language",
    y="Count",
    title="Top 10 Languages by Number of Originals",
    color_discrete_sequence=["#EF553B"],
    template="plotly_white",
)

fig_top_languages.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="Language"),
    yaxis=dict(title="Count"),
)

st.plotly_chart(fig_top_languages, use_container_width=True)

# 5. Skor IMDB dari waktu ke waktu
fig_scores_over_time = px.line(
    df_selection,
    x="Premiere",
    y="IMDB Score",
    title="IMDB Scores Over Time",
    template="plotly_white",
    color_discrete_sequence=["#AB63FA"]
)

fig_scores_over_time.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="Premiere Year"),
    yaxis=dict(title="IMDB Score"),
)

st.plotly_chart(fig_scores_over_time, use_container_width=True)

# 6. Hubungan durasi dan skor IMDB
fig_runtime_vs_score = px.scatter(
    df_selection,
    x="Runtime",
    y="IMDB Score",
    title="Relationship between Runtime and IMDB Score",
    template="plotly_white",
    color_discrete_sequence=["#00CC96"]
)

fig_runtime_vs_score.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="Runtime (minutes)"),
    yaxis=dict(title="IMDB Score"),
)

st.plotly_chart(fig_runtime_vs_score, use_container_width=True)
