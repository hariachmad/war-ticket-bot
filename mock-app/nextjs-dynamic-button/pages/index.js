import fs from "fs";
import path from "path";
import Head from "next/head";
import styles from "../styles/Home.module.css";

export async function getServerSideProps() {
  const filePath = path.join(process.cwd(), "config.json");
  const file = fs.readFileSync(filePath, "utf-8");
  const config = JSON.parse(file);

  return {
    props: { config },
  };
}

export default function Home({ config }) {
  return (
    <>
      <Head>
        <title>Ticket Sale Schedule</title>
      </Head>

      <main className={styles.main}>
        <div className={styles.grid}>
          {config.phases.map((phase, index) => (
            <div className={styles.column} key={index}>
              <h2 className={styles.columnTitle}>{phase.title}</h2>

              <button
                className={styles.button}
                style={{
                  backgroundColor: phase.buttonColor,
                  color: phase.buttonTextColor,
                  border: `2px solid ${phase.buttonBorderColor}`,
                }}
              >
                {phase.buttonLabel}
              </button>

              <p className={styles.startDate}>{phase.startDate}</p>
              <p className={styles.startTime}>{phase.startTime}</p>
            </div>
          ))}
        </div>

        <hr className={styles.divider} />
      </main>
    </>
  );
}
