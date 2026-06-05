module.exports = {
  apps: [
    {
      name: "stella",
      cwd: __dirname,
      script: "my_bot.py",
      interpreter: "./venv/bin/python",
      autorestart: true,
      max_restarts: 10,
      restart_delay: 5000,
      env: {
        NODE_ENV: "production",
      },
    },
  ],
};
